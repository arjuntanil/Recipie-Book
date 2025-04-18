from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View
from django.db.models import Q, Count
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout, update_session_auth_hash
from django.views.generic.edit import FormView
from django.http import JsonResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
import logging

from .models import Recipe, Ingredient, RecipeImage, SavedRecipe
from .forms import RecipeForm, IngredientFormSet, RecipeImageFormSet, UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm

logger = logging.getLogger(__name__)

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Recipe.objects.all()
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by difficulty
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Sort recipes
        sort = self.request.GET.get('sort', 'newest')
        if sort == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort == 'most_viewed':
            queryset = queryset.order_by('-view_count')
        elif sort == 'least_viewed':
            queryset = queryset.order_by('view_count')
        else:  # newest
            queryset = queryset.order_by('-created_at')
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories with their display names and counts
        categories = []
        for category_code, category_name in Recipe.CATEGORY_CHOICES:
            count = Recipe.objects.filter(category=category_code).count()
            categories.append({
                'code': category_code,
                'name': category_name,
                'count': count
            })
        
        context['categories'] = categories
        context['current_category'] = self.request.GET.get('category')
        
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        
        # Check if first view before incrementing counter
        if 'viewed_recipes' not in self.request.session:
            self.request.session['viewed_recipes'] = []
        
        self.is_first_view = str(obj.pk) not in self.request.session['viewed_recipes']
        
        # Use the model method to handle view counting
        obj.increment_view_count(self.request)
        
        return obj
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add flag to indicate if this is the first time viewing
        context['is_first_view'] = getattr(self, 'is_first_view', False)
        
        # Add saved recipes information
        if self.request.user.is_authenticated:
            saved_recipe = SavedRecipe.objects.filter(
                user=self.request.user,
                recipe=self.object
            ).exists()
            context['is_saved'] = saved_recipe
        
        return context

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipes:recipe-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = IngredientFormSet(self.request.POST, prefix='ingredients')
            context['image_formset'] = RecipeImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['ingredient_formset'] = IngredientFormSet(prefix='ingredients')
            context['image_formset'] = RecipeImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        image_formset = context['image_formset']
        
        with transaction.atomic():
            self.object = form.save()
            
            if ingredient_formset.is_valid():
                ingredient_formset.instance = self.object
                ingredient_formset.save()
            else:
                return self.form_invalid(form)
                
            if image_formset.is_valid():
                image_formset.instance = self.object
                image_formset.save()
            else:
                return self.form_invalid(form)
        
        messages.success(self.request, 'Recipe created successfully!')
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse('recipes:recipe-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = IngredientFormSet(
                self.request.POST, instance=self.object, prefix='ingredients'
            )
            context['image_formset'] = RecipeImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context['ingredient_formset'] = IngredientFormSet(instance=self.object, prefix='ingredients')
            context['image_formset'] = RecipeImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        image_formset = context['image_formset']
        
        if not ingredient_formset.is_valid():
            print("Ingredient formset errors:", ingredient_formset.errors)
            for i, err in enumerate(ingredient_formset.errors):
                if err:
                    print(f"Form {i} errors:", err)
            messages.error(self.request, 'There was an error with the ingredients. Please check the form.')
            return self.form_invalid(form)
            
        if not image_formset.is_valid():
            print("Image formset errors:", image_formset.errors)
            messages.error(self.request, 'There was an error with the images. Please check the form.')
            return self.form_invalid(form)
        
        with transaction.atomic():
            self.object = form.save()
            
            # Process ingredient formset
            # Instead of deleting all ingredients, let the formset handle deletions
            ingredient_formset.instance = self.object
            ingredient_formset.save()
            
            # Process each image form in the formset
            for image_form in image_formset:
                # Skip forms that haven't changed
                if not image_form.has_changed():
                    continue
                    
                # Handle deleted images
                if image_form.cleaned_data.get('DELETE', False):
                    if image_form.instance.pk:
                        image_form.instance.delete()
                # If it's a new image or an update
                elif image_form.cleaned_data.get('image') or image_form.instance.pk:
                    image = image_form.save(commit=False)
                    image.recipe = self.object
                    image.save()
        
        messages.success(self.request, 'Recipe updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Get the form errors to display to the user
        for field, error in form.errors.items():
            messages.error(self.request, f"{field}: {error}")
        
        return super().form_invalid(form)

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipes:recipe-list')
    
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recipe deleted successfully!')
        return super().delete(request, *args, **kwargs)

def search_recipes(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    cooking_time = request.GET.get('cooking_time', '')

    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredient_set__name__icontains=query)
        ).distinct()

    if category:
        recipes = recipes.filter(category=category)

    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)

    if cooking_time:
        recipes = recipes.filter(cooking_time__lte=int(cooking_time))

    context = {
        'recipes': recipes,
        'query': query,
        'categories': Recipe.CATEGORY_CHOICES,
        'difficulties': Recipe.DIFFICULTY_CHOICES,
        'selected_category': category,
        'selected_difficulty': difficulty,
        'selected_time': cooking_time,
    }

    return render(request, 'recipes/search_results.html', context)

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'recipes/login.html'
    
    def get_success_url(self):
        return reverse_lazy('recipes:recipe-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'You have been successfully logged in!')
        return super().form_valid(form)

class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'recipes/register.html'
    success_url = reverse_lazy('recipes:recipe-list')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, f'Account created for {user.username}! You are now logged in.')
        return super().form_valid(form)

def user_logout(request):
    """
    Custom logout view that logs out the user and redirects to the login page
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out!')
    return redirect('recipes:login')

def google_oauth_check(request):
    """
    Diagnostic view to check Google OAuth configuration
    """
    context = {}
    
    # Check if Google provider is configured
    google_app = SocialApp.objects.filter(provider='google').first()
    
    if google_app:
        context['google_configured'] = True
        context['app_name'] = google_app.name
        
        # Only show the first few characters of sensitive info
        client_id = google_app.client_id
        if client_id:
            context['client_id_preview'] = f"{client_id[:8]}...{client_id[-4:]}" if len(client_id) > 12 else "[Invalid]"
        
        client_secret = google_app.secret
        if client_secret:
            context['has_secret'] = True
            context['secret_preview'] = f"{client_secret[:4]}...{client_secret[-4:]}" if len(client_secret) > 8 else "[Invalid]"
        
        # Check site configuration
        sites = list(google_app.sites.all())
        current_site = Site.objects.get_current()
        
        context['sites'] = [site.domain for site in sites]
        context['current_site'] = current_site.domain
        context['site_matches'] = current_site in sites
        
        # Check callback URL - changed from within recipes app to project root level
        callback_url = f"http://{current_site.domain}/accounts/google/login/callback/"
        context['callback_url'] = callback_url
    else:
        context['google_configured'] = False
    
    return render(request, 'recipes/google_oauth_check.html', context)

class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'recipes/profile_edit.html'
    
    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = CustomPasswordChangeForm(request.user)
        
        # Check if user is authenticated through Google
        is_google_user = request.user.social_auth.filter(provider='google-oauth2').exists() if hasattr(request.user, 'social_auth') else False
        
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'password_form': password_form,
            'is_google_user': is_google_user,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        is_google_user = request.user.social_auth.filter(provider='google-oauth2').exists() if hasattr(request.user, 'social_auth') else False
        
        if 'password_change' in request.POST:
            if is_google_user:
                messages.error(request, 'Only manually created users can update their password. Google account users cannot change their password here.')
                return redirect('recipes:profile-edit')
                
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('recipes:profile-edit')
            else:
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=request.user.profile)
        else:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            password_form = CustomPasswordChangeForm(request.user)
            
            if u_form.is_valid() and p_form.is_valid():
                # Check if username is changed
                new_username = u_form.cleaned_data.get('username')
                if new_username != request.user.username:
                    # Check if the new username is available
                    if User.objects.filter(username__iexact=new_username).exclude(id=request.user.id).exists():
                        messages.error(request, 'This username is already taken.')
                        context = {
                            'u_form': u_form,
                            'p_form': p_form,
                            'password_form': password_form,
                            'is_google_user': is_google_user,
                        }
                        return render(request, self.template_name, context)
                
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('recipes:recipe-list')
            
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'password_form': password_form,
            'is_google_user': is_google_user,
        }
        
        return render(request, self.template_name, context)

def handler404(request, exception, template_name="404.html"):
    """
    Custom 404 handler
    """
    context = {
        'request_path': request.path
    }
    return render(request, template_name, context, status=404)

@login_required
def debug_profile(request):
    """
    Debug view to check the profile picture
    """
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_ROOT': settings.MEDIA_ROOT,
    }
    return render(request, 'recipes/debug_profile.html', context)

class HomeView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'featured_recipes'
    
    def get_queryset(self):
        # Get top 5 most viewed recipes
        return Recipe.objects.order_by('-view_count')[:5]

def clear_recipe_view_history(request):
    """
    Clear the user's recipe view history from their session.
    This allows users to reset which recipes are marked as "new".
    """
    if 'viewed_recipes' in request.session:
        del request.session['viewed_recipes']
        request.session.modified = True
        messages.success(request, 'Your recipe view history has been cleared. All recipes will appear as new again.')
    else:
        messages.info(request, 'No view history to clear.')
    
    # Redirect back to the referring page or recipe list
    next_url = request.GET.get('next', reverse('recipes:recipe-list'))
    return redirect(next_url)

def google_signin(request):
    """
    View to handle the intermediate Google sign-in page
    """
    return render(request, 'recipes/google_signin.html')

def check_username(request):
    """Check if a username is available."""
    username = request.GET.get('username', '').strip()
    current_user = request.user
    
    if not username:
        return JsonResponse({'available': False, 'message': 'Username cannot be empty'})
    
    if len(username) < 3:
        return JsonResponse({'available': False, 'message': 'Username must be at least 3 characters long'})
        
    if not username.isalnum() and '_' not in username:
        return JsonResponse({'available': False, 'message': 'Username can only contain letters, numbers, and underscores'})
    
    # Check if username exists but exclude current user
    exists = User.objects.filter(Q(username__iexact=username) & ~Q(id=current_user.id)).exists()
    
    if exists:
        return JsonResponse({'available': False, 'message': 'This username is already taken'})
    
    return JsonResponse({'available': True, 'message': 'Username is available'})

class MyRecipesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/my_recipes.html'
    context_object_name = 'user_recipes'
    paginate_by = 12
    
    def get_queryset(self):
        # Only return recipes created by the logged-in user
        return Recipe.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_recipes'] = self.get_queryset().count()
        return context

class SavedRecipesView(LoginRequiredMixin, ListView):
    model = SavedRecipe
    template_name = 'recipes/saved_recipes.html'
    context_object_name = 'saved_recipes'
    
    def get_queryset(self):
        return SavedRecipe.objects.filter(user=self.request.user)

def toggle_save_recipe(request, recipe_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    saved_recipe, created = SavedRecipe.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )
    
    if not created:
        # Recipe was already saved, so unsave it
        saved_recipe.delete()
        return JsonResponse({
            'is_saved': False,
            'message': 'Recipe removed from your saved collection'
        })
    
    return JsonResponse({
        'is_saved': True,
        'message': 'Recipe saved successfully!'
    })
