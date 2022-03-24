from django import template
from django.contrib.auth.models import Group

from datetime import datetime

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter(name='readable_date')
def readable_date(date):
    return (datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S'))

@register.filter(name='per_cent')
def percentagement(value):
    return (value * 100)
