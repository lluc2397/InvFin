from django.template import Library

from ..utils import HostChecker

register = Library()

UNSET = object()


@register.simple_tag(takes_context=True)
def url(context, view, subdomain=UNSET, *args, **kwargs):
    if subdomain is UNSET:
        request = context.get('request')
        if request is not None:
            subdomain = getattr(request, 'subdomain', None)
        else:
            subdomain = None
    elif subdomain == '':
        subdomain = None

    return HostChecker(request).reverse(view, subdomain=subdomain, args=args, kwargs=kwargs)