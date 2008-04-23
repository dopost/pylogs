from django.template import Library
import datetime

register = Library()

def time_before_now(value,args=None):
    '''calc the time before now'''
    return datetime.datetime().strftime('%y')

register.filter('time_before_now',time_before_now)

def priority_name(value):
    '''return priority name'''    
    if value == 2:      
        return 'high'
    elif value == 1:
        return 'medium'
    else:
        return 'low'    
register.filter('priority_name',priority_name)