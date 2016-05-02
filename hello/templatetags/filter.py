from datetime import datetime

from django import template

register = template.Library()

@register.filter("timestamp")
def timestamp(value):
    try:
        return datetime.fromtimestamp(float(value)).strftime('%d-%m-%Y %H:%M:%S')
    except AttributeError, e:
        return datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    except ValueError, e:
        return '01-01-1970 00:00:00'

@register.filter("array_to_string")
def array_to_string(array):
    str = ''
    for value in array:
        str += value + ' '
    str = str[:len(str)-1]
    return str