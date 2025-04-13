from django.contrib import admin
from .models import Recipe, Ingredient, RecipeImage

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'preparation_time', 'cooking_time', 'created_at')
    search_fields = ('name',)
    inlines = [IngredientInline, RecipeImageInline]

@admin.register(RecipeImage)
class RecipeImageAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary',)
