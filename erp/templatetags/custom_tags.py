from django import template

register = template.Library()

@register.filter
def has_role(user, roles):
    role_list = [role.strip() for role in roles.split(",")]
    return getattr(user, 'role', None) in role_list