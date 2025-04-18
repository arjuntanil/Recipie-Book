from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', default='default.jpg')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Check if profile picture exists
        if self.profile_picture and os.path.exists(self.profile_picture.path):
            img = Image.open(self.profile_picture.path)
            if img.height > 150 or img.width > 150:
                output_size = (150, 150)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)

class Recipe(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    
    CATEGORY_CHOICES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('dessert', 'Dessert'),
        ('snack', 'Snack'),
        ('beverage', 'Beverage'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    preparation_steps = models.TextField()
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    servings = models.PositiveIntegerField(default=4)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def total_time(self):
        return self.preparation_time + self.cooking_time
        
    def increment_view_count(self, request):
        """
        Increment the view count only if this user/session hasn't viewed this recipe before.
        Returns True if the view count was incremented, False otherwise.
        """
        # Initialize viewed_recipes in session if it doesn't exist
        if 'viewed_recipes' not in request.session:
            request.session['viewed_recipes'] = []
        
        # Get list of recipes this user has already viewed
        viewed_recipes = request.session['viewed_recipes']
        
        # Only increment view count if this user hasn't viewed this recipe before
        if str(self.pk) not in viewed_recipes:
            self.view_count += 1
            self.save(update_fields=['view_count'])
            
            # Add this recipe to user's viewed list
            viewed_recipes.append(str(self.pk))
            request.session['viewed_recipes'] = viewed_recipes
            request.session.modified = True
            return True
            
        return False

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient_set')
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name}"

class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipeimage_set')
    image = models.ImageField(upload_to='recipe_images/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.recipe.name}"
    
    def save(self, *args, **kwargs):
        # If this image is marked as primary, make all other images non-primary
        if self.is_primary:
            RecipeImage.objects.filter(recipe=self.recipe).update(is_primary=False)
        
        # If no images for this recipe are primary, make this one primary
        elif not RecipeImage.objects.filter(recipe=self.recipe, is_primary=True).exists():
            self.is_primary = True
            
        super().save(*args, **kwargs)

class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')  # Prevent duplicate saves
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.name}"
