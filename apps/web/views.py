from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.views.generic import (
    TemplateView,
    FormView,
    DetailView)

import json
import urllib

from apps.emailing.views import BaseNewsletterView
from apps.web.models import WebsiteLegalPage, WebsiteEmailsType, WebsiteEmail
from apps.public_blog.models import WritterProfile
from apps.public_blog.views import writter_profile_view
from apps.general.utils import HostChecker

from .forms import ContactForm

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


def soporte_view(request):    
    form = ContactForm()
    public_key = settings.GOOGLE_RECAPTCHA_PUBLIC_KEY
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
                # SEND_EMAIL_FOR_CONTACT(nombre, email, comentario, peticion)
                return redirect ('web:soporte')

        messages.error(request, 'Ha habido un error')
        return redirect ('web:soporte')

    return render(request, 'web_principal/soporte.html', {'form':form, 'public_key':public_key})


class ExcelView(TemplateView):
    template_name = 'web_principal/excel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateWebEmailView(BaseNewsletterView, FormView):
    model = WebsiteEmail	
    template_name = 'web_principal/mandar_emails.html'

    def get_success_url(self) -> str:
        return reverse("users:user_inicio")

    def form_valid(self, form):
        form.send_email(self.model)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

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