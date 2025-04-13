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

from .models import Recipe, Ingredient, RecipeImage
from .forms import RecipeForm, IngredientFormSet, RecipeImageFormSet, UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 9
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category if provided
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        # Filter by user if provided
        user_id = self.request.GET.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add category to context if filtered
        if self.request.GET.get('category'):
            context['current_category'] = self.request.GET.get('category')
        
        # Add user filter to context
        if self.request.GET.get('user'):
            context['user_filtered'] = True
            
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # Increment view count
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipe-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = IngredientFormSet(self.request.POST)
            context['image_formset'] = RecipeImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['ingredient_formset'] = IngredientFormSet()
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
        return reverse('recipe-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = IngredientFormSet(
                self.request.POST, instance=self.object
            )
            context['image_formset'] = RecipeImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context['ingredient_formset'] = IngredientFormSet(instance=self.object)
            context['image_formset'] = RecipeImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        image_formset = context['image_formset']
        
        with transaction.atomic():
            self.object = form.save()
            
            if ingredient_formset.is_valid():
                ingredient_formset.save()
            else:
                return self.form_invalid(form)
                
            if image_formset.is_valid():
                image_formset.save()
            else:
                return self.form_invalid(form)
        
        messages.success(self.request, 'Recipe updated successfully!')
        return super().form_valid(form)

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe-list')
    
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recipe deleted successfully!')
        return super().delete(request, *args, **kwargs)

def search_recipes(request):
    query = request.GET.get('q', '')
    if query:
        # Search in recipe names, descriptions, and ingredients
        recipes = Recipe.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(ingredients__name__icontains=query)
        ).distinct()
    else:
        recipes = Recipe.objects.all()
    
    context = {
        'recipes': recipes,
        'query': query
    }
    return render(request, 'recipes/search_results.html', context)

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'recipes/login.html'
    
    def get_success_url(self):
        return reverse_lazy('recipe-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'You have been successfully logged in!')
        return super().form_valid(form)

class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'recipes/register.html'
    success_url = reverse_lazy('recipe-list')
    
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
    return redirect('login')

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
        
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'password_form': password_form,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        if 'password_change' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile-edit')
            else:
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=request.user.profile)
        else:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            password_form = CustomPasswordChangeForm(request.user)
            
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('recipe-list')
            
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'password_form': password_form,
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
    template_name = 'home.html'
    context_object_name = 'featured_recipes'
    
    def get_queryset(self):
        # Get top 5 most viewed recipes
        return Recipe.objects.order_by('-view_count')[:5]
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add categories to context
        context['categories'] = Recipe.CATEGORY_CHOICES
        
        # Add category counts to context
        category_counts = {}
        for category, _ in Recipe.CATEGORY_CHOICES:
            count = Recipe.objects.filter(category=category).count()
            category_counts[category] = count
        context['category_counts'] = category_counts
        
        return context
