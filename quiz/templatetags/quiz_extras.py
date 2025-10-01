from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Returns the value from a dictionary for a given key.
    Usage: {{ my_dict|get_item:key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def div(value, arg):
    """
    Divides the value by the arg.
    Usage: {{ value|div:arg }}
    """
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def index(indexable, i):
    """
    Returns the item at index i from the indexable object.
    Usage: {{ my_list|index:i }}
    """
    try:
        return indexable[i]
    except (IndexError, TypeError):
        return None