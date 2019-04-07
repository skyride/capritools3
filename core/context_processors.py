from django.conf import settings

from .navigation import navigation_controller


def presentation(request):
    """Adds context for the purpose of presentation."""
    return {
        'nav_title': settings.TITLE,
        'theme': "flatly",
        'VIEW_CACHE_TIME': settings.VIEW_CACHE_TIME
    }


def navigation(request):
    """Adds context for our navigation barrr"""
    return {
        'navigation_controller': navigation_controller
    }