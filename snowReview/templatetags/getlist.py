from django import template

register = template.Library()

@register.filter
def getlist(value, arg):
    return value.getlist(arg)