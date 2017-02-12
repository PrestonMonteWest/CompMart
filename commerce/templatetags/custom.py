from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
@stringfilter
def cut(value, arg):
    '''
    Remove all instances of arg from value.
    '''

    return value.replace(arg, '')
