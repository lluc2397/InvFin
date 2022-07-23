import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import (
    CreateView, 
    DetailView,
    RedirectView
)

from apps.general.utils import HostChecker
from apps.public_blog.models import WritterProfile
from apps.seo.views import SEOTemplateView
from apps.web.models import WebsiteLegalPage

from .forms import ContactForm, WebEmailForm


class HomePage(SEOTemplateView):    
    def render_to_response(self, context, **response_kwargs):
        writter = HostChecker(self.request).return_writter()
        if writter:
            context.update(
                {
            "meta_desc": writter.user_profile.bio,
            "meta_title": writter.full_name,
            "meta_img": writter.foto,
            "current_profile": writter
        }
            )
            template_name = 'profile/public/profile.html'
        else:
            escritores = WritterProfile.objects.all()
            context['escritor1'] = escritores[0]
            context['escritor2'] = escritores[1]
            context['escritor3'] = escritores[2]
            template_name = 'home_page.html'

        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=[template_name],
            context=context,
            using=self.template_engine,
            **response_kwargs
        )


class LegalPages(DetailView):
    template_name = 'legals.html'
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

    return render(request, 'soporte.html', context)


class ExcelRedirectView(RedirectView):
    permanent = True
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse("business:product", kwargs={"slug": "excel-inteligente-inifito"})


class CreateWebEmailView(CreateView):
    form_class = WebEmailForm
    template_name = 'mandar_emails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self) -> str:
        return reverse("users:user_inicio")

    def test_func(self):
        valid = False
        if self.request.user.is_superuser:
            valid = True
        return valid


def handler403(request, exception):
    return render(request, 'errors/403.html')


def handler404(request, exception):
    return render(request, 'errors/404.html')


def handler500(request):
    return render(request, 'errors/500.html')