from django import template
from ..models import CATEGORIES

register = template.Library()

@register.simple_tag
def define(val=None):
  return val

@register.filter(name='categories')
def categories(value):
    return CATEGORIES

@register.filter(name='remainder')
def remainder(value, arg):
    try:
        return value % arg
    except (ValueError, ZeroDivisionError):
        return None
    
@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg