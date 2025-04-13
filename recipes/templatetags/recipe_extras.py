from django import template

register = template.Library()

@register.filter
def addcss(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by its key"""
    return dictionary.get(key) 