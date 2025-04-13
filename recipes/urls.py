from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe-list'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/new/', views.RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/edit/', views.RecipeUpdateView.as_view(), name='recipe-update'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe-delete'),
    path('search/', views.search_recipes, name='recipe-search'),
    
    # Profile URLs
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/debug/', views.debug_profile, name='debug-profile'),
    
    # Authentication URLs
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    
    # Google OAuth Setup Guides
    path('setup-google-oauth/', TemplateView.as_view(template_name='setup_google_oauth.html'), name='setup-google-oauth'),
    
    # Google OAuth Diagnostic
    path('google-oauth-check/', views.google_oauth_check, name='google-oauth-check'),
] 