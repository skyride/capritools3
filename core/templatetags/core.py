from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
@stringfilter
def startswith(value, arg):
    return value.startswith(arg)


@register.filter
def gentolist(generator):
    """
    Used to turn a generator into a list so we don't have to execute it
    multiple times when its used in multiple locations or to get its length.
    """
    return list(generator)