from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
import base64
from django.utils import timezone
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
	UpdateView,
	CreateView)
from django.apps import apps

from .models import WritterNewsletterDefaultOptions
from .forms import DefaultNewsletterForm, DefaultNewsletterFieldsForm

def email_opened_view(request, uidb64):
    
    pixel_gif = base64.b64decode(b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=')
    
    if request.method == 'GET':
        decoded_url = force_text(urlsafe_base64_decode(uidb64)).split("-")
        id, app_label, object_name = decoded_url[0], decoded_url[1], decoded_url[2]
        modelo = apps.get_model(app_label, object_name, require_ready=True).objects.get(id=id)
        modelo.opened = True
        modelo.date_opened = timezone.now()
        modelo.save()
        return HttpResponse(pixel_gif, content_type='image/gif')



class BaseNewsletterView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin):
    form_class = DefaultNewsletterForm
    context_object_name = "newsletter_form"
    success_message = 'Newsletter creada'

    def get_initial_default_newsletter(self):
        initial = {}
        user_default_options = self.request.user.default_options
        if user_default_options != False:
            initial['title'] = user_default_options.title.content
            initial['intro'] = user_default_options.intro.content
            initial['despedida'] = user_default_options.despedida.content
        return initial
    
    def get_default_initial_with_content(self, content):
        initial = self.get_initial_default_newsletter()
        initial['content'] = content.content
        return initial
    
    def get_initial(self, *args, **kwargs):
        default_newsletter = self.get_initial_default_newsletter()
        
        return default_newsletter

    def form_valid(self, form):
        form.annotate_changes(self.request.user)
        return super().form_valid(form)

    def can_create_newsl(self):
        valid = False
        if self.request.user.is_writter or self.request.user.is_superuser:
            valid = True
        return valid

    def test_func(self):
        return self.can_create_newsl()

    def handle_no_permission(self):
        return redirect("preguntas_respuestas:list_questions")


class CreateDefaultFieldView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = WritterNewsletterDefaultOptions
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



	