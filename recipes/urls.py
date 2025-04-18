from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'recipes'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe-list'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/new/', views.RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/edit/', views.RecipeUpdateView.as_view(), name='recipe-update'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe-delete'),
    path('search/', views.search_recipes, name='search'),
    path('clear-view-history/', views.clear_recipe_view_history, name='clear-view-history'),
    
    # Profile URLs
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/check-username/', views.check_username, name='check-username'),
    path('profile/debug/', views.debug_profile, name='debug-profile'),
    
    # Authentication URLs
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    
    # Google OAuth Setup Guides
    path('setup-google-oauth/', TemplateView.as_view(template_name='setup_google_oauth.html'), name='setup-google-oauth'),
    
    # Google OAuth Diagnostic
    path('google-oauth-check/', views.google_oauth_check, name='google-oauth-check'),
    
    # Google Sign-in
    path('google/signin/', views.google_signin, name='google-signin'),
    path('my-recipes/', views.MyRecipesView.as_view(), name='my_recipes'),
    path('saved-recipes/', views.SavedRecipesView.as_view(), name='saved_recipes'),
    path('toggle-save/<int:recipe_id>/', views.toggle_save_recipe, name='toggle_save_recipe'),
] 