#!/usr/bin/env python
from django.template import Library
register = Library()
def media_url():
    """
    Returns the string contained in the setting MEDIA_PREFIX.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.MEDIA_URL
media_url = register.simple_tag(media_url)

def theme_media_url():
    """
    Returns the themes media url
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.MEDIA_URL + settings.THEME_NAME
theme_media_url = register.simple_tag(theme_media_url)
    