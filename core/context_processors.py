from django.conf import settings


def presentation(request):
    """
    Adds context for the purpose of presentation.
    """
    return {
        'nav_title': settings.TITLE,
        'theme': "flatly"
    }