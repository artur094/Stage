from datetime import datetime

from django import template

register = template.Library()

@register.filter("timestamp")
def timestamp(value):
    try:
        return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
    except AttributeError, e:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')