from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
import functools
from urllib.parse import urlunparse
from django.conf import settings
from django.urls import reverse as simple_reverse

import binascii
import os
import csv
import random

from apps.public_blog.models import WritterProfile

User = get_user_model()
FULL_DOMAIN = settings.FULL_DOMAIN


class ChartSerializer:
    def generate_json(self, comparing_json:dict, items:list=None, chart_type:str='line')->dict:
        labels = comparing_json['labels']
        chartData = {
            'labels': labels,
            'fields': []
        }
        if not items:
            items = [i for i in range(len(comparing_json['fields']))]

        fields_for_chart = [comparing_json['fields'][num] for num in items]

        for field in fields_for_chart:
            comparaison_dict = {
                    'label': field['title'],
                    'data': field['values'],
                    'backgroundColor': '',
                        'borderColor': '',
                    
                    'yAxisID':"right",
                    'order': 0,
                    'type': chart_type
            }
            chartData['fields'].append(comparaison_dict)
        
        return chartData

    def generate_portfolio_charts(self):
        data = {
            'labels': [],
            'datasets': [
                {
                'label': '',
                'data': 0,
                'backgroundColor': "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)]),
                }
            ]
        }


class HostChecker:
    def __init__(self, request) -> None:
        self.request = request
        self.host = self.request.get_host().split('.')[0]
        self.current_domain = FULL_DOMAIN
    

    def check_writter(self):
        if WritterProfile.objects.filter(host_name = self.host).exists():
            return self.host
        else:
            return False
    
    def check_host(self):
        if self.host != self.current_domain and self.host != "www":
            return False
    
    def correct_host(self):
        if self.check_host() == False and self.check_writter == False:
            return FULL_DOMAIN


class ExportCsv:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        meta = f'{meta}'.replace('.', '-')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export to csv"


class UniqueCreator:
    @classmethod
    def create_unique_field(cls, model, value, field, original_value=None, extra:int = 0):
        if model.__class__.objects.filter(**{field:value}).exists():
            if field == 'key':
                value = UniqueCreator.generate_key()
            else:
                value = UniqueCreator.generate_slug(original_value, extra)
            return UniqueCreator.create_unique_field(value, field)
        return value
    
    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()
    
    @classmethod
    def generate_slug(cls, value=None, extra:int = 0):
        extra += 1
        return slugify(value + str(extra))


def current_site_domain():
    domain = settings.CURRENT_DOMAIN

    prefix = 'www.'
    if getattr(settings, 'REMOVE_WWW_FROM_DOMAIN', False) \
            and domain.startswith(prefix):
        domain = domain.replace(prefix, '', 1)

    return domain


get_domain = current_site_domain


def urljoin(domain, path=None, scheme=None):
  """
  Joins a domain, path and scheme part together, returning a full URL.
  :param domain: the domain, e.g. ``example.com``
  :param path: the path part of the URL, e.g. ``/example/``
  :param scheme: the scheme part of the URL, e.g. ``http``, defaulting to the
      value of ``settings.DEFAULT_URL_SCHEME``
  :returns: a full URL
  """
  if scheme is None:
    scheme = getattr(settings, 'DEFAULT_URL_SCHEME', 'http')

  return urlunparse((scheme, domain, path or '', None, None, None))


def reverse(viewname, subdomain=None, scheme=None, args=None, kwargs=None,
            current_app=None):
  """
  Reverses a URL from the given parameters, in a similar fashion to
  :meth:`django.core.urlresolvers.reverse`.
  :param viewname: the name of URL
  :param subdomain: the subdomain to use for URL reversing
  :param scheme: the scheme to use when generating the full URL
  :param args: positional arguments used for URL reversing
  :param kwargs: named arguments used for URL reversing
  :param current_app: hint for the currently executing application
  """
  urlconf = settings.SUBDOMAIN_URLCONFS.get(subdomain, settings.ROOT_URLCONF)

  domain = get_domain()
  if subdomain is not None:
    domain = '%s.%s' % (subdomain, domain)

  path = simple_reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs,
                        current_app=current_app)
  return urljoin(domain, path, scheme=scheme)


#: :func:`reverse` bound to insecure (non-HTTPS) URLs scheme
insecure_reverse = functools.partial(reverse, scheme='http')

#: :func:`reverse` bound to secure (HTTPS) URLs scheme
secure_reverse = functools.partial(reverse, scheme='https')

#: :func:`reverse` bound to be relative to the current scheme
relative_reverse = functools.partial(reverse, scheme='')