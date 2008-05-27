#!/usr/bin/env python
#coding=utf-8
#global config
from django.template import Library
import pylogs
register = Library()

def get_version():
    """
    Returns the pylogs version
    """    
    return pylogs.get_version()
register.simple_tag(get_version)