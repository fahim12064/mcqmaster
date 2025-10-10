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
    Divides the value by the arg. Safely handles ZeroDivisionError.
    """
    try:
        value = float(value)
        arg = float(arg)
        
        if arg == 0:
            return 0
            
        return value / arg
    except (ValueError, TypeError):
        return None



@register.filter
def mul(value, arg):
    """Multiplies the value by the arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return None
