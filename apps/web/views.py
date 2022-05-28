from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView)

import json
import urllib

from apps.web.models import WebsiteLegalPage
from apps.public_blog.models import WritterProfile
from apps.public_blog.views import writter_profile_view
from apps.general.utils import HostChecker

from .forms import ContactForm, WebEmailForm


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
        long = '12345'
        print(long[-2:])
        return context


class LegalPages(DetailView):
    template_name = 'web_principal/legals.html'
    model = WebsiteLegalPage
    context_object_name = "object"
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_desc"] = 'Todo lo que necesitas para ser un mejor inversor'
        context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir'
        context["meta_title"] = 'Invierte correctamente'
        context["meta_url"] = ''
        return context


def soporte_view(request):
    initial = {}
    if request.user.is_authenticated:
        initial['name'] = request.user.username
        initial['email'] = request.user.email
    form = ContactForm(initial=initial)
    public_key = settings.GOOGLE_RECAPTCHA_PUBLIC_KEY
    context = {
        'form':form, 
        'public_key':public_key,
        'meta_title':'Soporte'}
        
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())

            if result['success']:
                messages.success(request, 'Gracias por tu mensaje, te responderemos lo antes posible.')
                form.send_email()
                return redirect ('web:soporte')

        messages.error(request, 'Ha habido un error')
        return redirect ('web:soporte')

    return render(request, 'web_principal/soporte.html', context)


class ExcelView(TemplateView):
    template_name = 'web_principal/excel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_desc"] = 'El mejor excel para invertir correctamente y obtener mejores beneficios'
        context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir, excel'
        context["meta_title"] = 'Excel inteligente'
        context["meta_url"] = 'excel-analisis/'
        return context


class CreateWebEmailView(CreateView):
    form_class = WebEmailForm
    
    template_name = 'web_principal/mandar_emails.html'

    def get_success_url(self) -> str:
        return reverse("users:user_inicio")

    def test_func(self):
        valid = False
        if self.request.user.is_superuser:
            valid = True
        return valid


def handler403(request, exception):
    return render(request, 'general/errors/403.html')


def handler404(request, exception):
    return render(request, 'general/errors/404.html')


def handler500(request):
    return render(request, 'general/errors/500.html')