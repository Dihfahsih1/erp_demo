from django import template

register = template.Library()

# @register.filter
# def percentage(value, arg):
#     try:
#         return round((float(value) / float(arg)) * 100, 2)
#     except (ValueError, ZeroDivisionError):
#         return 0
    
@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
    
    
register.filter
def percentage(value, total):
    try:
        if total and float(total) > 0:
            return (float(value) / float(total)) * 100
        return 0
    except (ValueError, TypeError):
        return 0