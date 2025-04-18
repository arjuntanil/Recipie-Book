from django import template
from django.utils.html import format_html
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using bracket notation.
    Usage: {{ mydict|get_item:item_key }}
    """
    return dictionary.get(key, 0)

@register.filter
def format_time(minutes):
    """
    Format minutes into a human-readable time string
    Example: 75 minutes becomes "1h 15m"
    """
    if not minutes:
        return "N/A"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if hours > 0 and remaining_minutes > 0:
        return f"{hours}h {remaining_minutes}m"
    elif hours > 0:
        return f"{hours}h"
    else:
        return f"{minutes}m"

@register.filter
def difficulty_badge(level):
    """
    Format the difficulty level as a colored badge
    """
    if not level:
        return "N/A"
    
    level = level.lower()
    
    if level == 'easy':
        color = 'bg-success'
    elif level == 'medium':
        color = 'bg-warning'
    elif level == 'hard':
        color = 'bg-danger'
    else:
        color = 'bg-secondary'
    
    return format_html('<span class="badge rounded-pill {}">{}</span>', color, level.capitalize())

@register.filter
def stars(value, max_stars=5):
    """
    Convert a numerical value to star rating HTML
    Example: 3.5 out of 5 will show 3 full stars, 1 half star, and 1 empty star
    """
    if not value:
        value = 0
    
    try:
        value = float(value)
    except (ValueError, TypeError):
        return "Invalid rating"
    
    full_stars = int(value)
    half_star = False
    
    if value - full_stars >= 0.5:
        half_star = True
    
    empty_stars = max_stars - full_stars - (1 if half_star else 0)
    
    result = []
    
    # Full stars
    for i in range(full_stars):
        result.append('<i class="fas fa-star text-warning"></i>')
    
    # Half star
    if half_star:
        result.append('<i class="fas fa-star-half-alt text-warning"></i>')
    
    # Empty stars
    for i in range(empty_stars):
        result.append('<i class="far fa-star text-warning"></i>')
    
    return format_html(''.join(result))

@register.filter
def percentage(value, max_value=100):
    """
    Convert a value to percentage width for progress bars
    """
    if not value:
        return "0%"
    
    try:
        percentage = (float(value) / float(max_value)) * 100
        return f"{min(percentage, 100)}%"
    except (ValueError, TypeError):
        return "0%"

@register.filter
def split_steps(value):
    """Split recipe steps by line breaks and filter out empty lines"""
    if value:
        return [step for step in value.splitlines() if step.strip()]
    return []

@register.simple_tag
def has_viewed_recipe(request, recipe_id):
    """Check if the current user/session has already viewed this recipe"""
    if not request or not recipe_id:
        return False
        
    viewed_recipes = request.session.get('viewed_recipes', [])
    return str(recipe_id) in viewed_recipes 

@register.filter
def split(value, arg):
    """
    Splits the value on the argument and returns a list.
    
    Usage: {{ value|split:"delimiter" }}
    Example: {{ "a,b,c"|split:"," }} -> ["a", "b", "c"]
    """
    return value.split(arg)

@register.filter
def strip(value):
    """
    Strips leading and trailing whitespace from a string.
    
    Usage: {{ value|strip }}
    Example: {{ "  text  "|strip }} -> "text"
    """
    return str(value).strip() 