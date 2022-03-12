from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
import base64
from django.utils import timezone
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
	ListView,
	TemplateView,
	DetailView,
	UpdateView,
	CreateView)

from .forms import NewsletterForm, DefaultNewsletterFieldsForm

def email_opened_view(request, uidb64):
    
    pixel_gif = base64.b64decode(b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=')
    
    if request.method == 'GET':
        id_title = force_text(urlsafe_base64_decode(uidb64))
        id = id_title.split("-")[0]
        title = id_title.split("-")[1]
        # if Newsletter.objects.filter(title = title).exists():
        #     newsletter = Newsletter.objects.get(title = title)
        #     NEWSLETTER_ACCURACY.objects.filter(email_related=newsletter, id = id).update(opened = True, date_opened=timezone.now())
           
        # else:
        #     EMAILS_ACCURACY.objects.filter(id = id).update(opened = True, date_opened=timezone.now())
            
        return HttpResponse(pixel_gif, content_type='image/gif')



class BaseNewsletterView(LoginRequiredMixin, UserPassesTestMixin):
    form_class = NewsletterForm

    def get_initial(self, *args, **kwargs):
        initial = super(BaseNewsletterView, self).get_initial(**kwargs)
        initial['title'] = '¿Cuál es tu pregunta?'
        initial['content'] = 'Explica tu duda con todo lujo de detalles'
        return initial

    def can_create_newsl(self):
        valid = False
        if self.request.user.is_writter or self.request.user.is_superuser:
            valid = True
        return valid

    def test_func(self):
        return self.can_create_newsl()


class CreateDefaultFieldView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = DefaultNewsletterFieldsForm
    context_object_name = "newsletter_fields_form"

    def form_valid(self, form):
        return super(CreateDefaultFieldView, self).form_valid(form)


class UpdateDefaultFieldView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	form_class = DefaultNewsletterFieldsForm
	context_object_name = "newsletter_fields_form"
	success_message = 'Escrito actualizado'
	template_name = 'public_blog/forms/update.html'

	def get_context_data(self, **kwargs):
		context = super(UpdateDefaultFieldView, self).get_context_data(**kwargs)        
		context['current_tags'] = self.get_object().tags.all()
		return context

	def form_valid(self, form):
		return super(UpdateDefaultFieldView, self).form_valid(form)



	