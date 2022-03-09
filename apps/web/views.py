from django.shortcuts import render
from django.views.generic import (
    TemplateView, 
    DetailView)

from apps.web.models import WebsiteLegalPage
from apps.public_blog.models import WritterProfile
from apps.public_blog.views import writter_profile_view
from apps.general.utils import HostChecker


class HomePage(TemplateView):
    template_name = 'web_principal/inicio.html'

    def get(self, request, *args, **kwargs):
        host = HostChecker(request).check_writter()
        if host != False:
            return writter_profile_view(request, host)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        escritores = WritterProfile.objects.all()
        context["meta_desc"] = 'Todo lo que necesitas para ser un mejor inversor'
        context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir'
        context["meta_title"] = 'Invierte correctamente'
        context["meta_url"] = ''
        context['escritor1'] = escritores[0]
        context['escritor2'] = escritores[1]
        context['escritor3'] = escritores[2]
        return context


class LegalPages(DetailView):
    template_name = 'web_principal/legals.html'
    model = WebsiteLegalPage
    context_object_name = "object"
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[''] = ''
        return context


class SoporteView(TemplateView):
    template_name = 'web_principal/soporte.html'


class ExcelView(TemplateView):
    template_name = 'web_principal/excel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def handler403(request, exception):
    return render(request, 'general/errors/403.html')


def handler404(request, exception):
    return render(request, 'general/errors/404.html')


def handler500(request):
    return render(request, 'general/errors/500.html')