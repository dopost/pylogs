#!/usr/bin/env python
#coding=utf-8
#global config
from django.template import Library
register = Library()


def do_get_version():
    """
    Returns the pylogs version
    """    
    return pylogs.get_version()
get_version = register.simple_tag(do_get_version)