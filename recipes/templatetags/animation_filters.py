from django import template
from django.utils.html import format_html
import re
import random

register = template.Library()

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
def animate_delay(index, base_delay=100):
    """
    Generate appropriate animation delay based on index
    Example: animate_delay:3 generates "delay-300"
    """
    delay = int(base_delay) * int(index)
    return f"delay-{delay}"

@register.filter
def format_steps(steps_text):
    """
    Format recipe steps text into well-structured HTML
    - Split by line breaks
    - Remove empty lines
    - Add numbering
    """
    if not steps_text:
        return ""
    
    steps = [step.strip() for step in steps_text.split('\n') if step.strip()]
    
    result = []
    for i, step in enumerate(steps):
        result.append(format_html(
            '<div class="instruction-item scroll-reveal delay-{}">'
            '<div class="instruction-number">{}</div>'
            '<div class="instruction-text">{}</div>'
            '</div>',
            (i+1)*100, i+1, step
        ))
    
    return format_html(''.join(result))

@register.filter
def truncate_chars(value, max_length):
    """
    Truncate text to specified character count preserving whole words
    """
    if not value:
        return ""
    
    if len(value) <= max_length:
        return value
    
    # Truncate to max_length, then find the last space before that point
    truncated = value[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space != -1:
        truncated = truncated[:last_space]
    
    return truncated + "..."

@register.filter
def word_highlight(text, highlight_words=1):
    """
    Highlight the first N words of text with special styling
    """
    if not text:
        return ""
        
    words = text.split()
    
    try:
        num_words = int(highlight_words)
    except (ValueError, TypeError):
        num_words = 1
    
    if len(words) <= num_words:
        return format_html('<span class="text-highlight">{}</span>', text)
    
    highlighted = ' '.join(words[:num_words])
    rest = ' '.join(words[num_words:])
    
    return format_html('<span class="text-highlight">{}</span> {}', highlighted, rest)

@register.filter
def elegant_quote(text):
    """
    Format text as an elegant quote with proper styling and quotation marks
    """
    if not text:
        return ""
    
    return format_html(
        '<div class="elegant-quote">'
        '<span class="quote-mark quote-open">&ldquo;</span>'
        '<span class="quote-content">{}</span>'
        '<span class="quote-mark quote-close">&rdquo;</span>'
        '</div>',
        text
    )

@register.filter
def random_animation_class(seed=None):
    """
    Return a random animation class for visual variety
    """
    animations = [
        'fade-up', 
        'fade-right', 
        'fade-left', 
        'zoom-in',
        'slide-up',
        'bounce-in'
    ]
    
    if seed:
        # Use seed to create deterministic randomness
        random.seed(str(seed))
        
    return random.choice(animations)

@register.simple_tag
def ingredient_animation(index):
    """
    Apply special staggered animation timing for ingredients list
    """
    delay = 100 + (50 * index)
    return format_html('scroll-reveal delay-{}', delay) 