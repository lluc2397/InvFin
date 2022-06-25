import json

from django import template
from django.contrib.auth.models import Group
from django.utils.html import strip_tags, format_html

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
    

@register.simple_tag(name='utm')
def add_utms(content='', term='', medium='webapp', source='invfin', campaign='website-links'):
    utm_source = f'utm_source={source}'
    utm_medium = f'utm_medium={medium}'
    utm_campaign = f'utm_campaign={campaign}'
    utm_content = f'utm_content={content}'
    utm_term = f'utm_term={term}'
    return f'?{utm_source}&{utm_medium}&{utm_content}&{utm_campaign}&{utm_term}'


@register.simple_tag(name='clean_json')
def api_json_example(example):
    print(type(example))
    parsed = json.loads(example)
    print(parsed)
    return json.dumps(example, indent=4, sort_keys=True)