from django.shortcuts import redirect, render
from django.contrib import messages
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import (
	ListView,
	TemplateView,
	DetailView,
	UpdateView,
	CreateView)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

from apps.emailing.views import BaseNewsletterView
from apps.emailing.forms import DefaultNewsletterFieldsForm

from .models import (
    PublicBlog,
    WritterProfile,
	PublicBlogAsNewsletter,
	NewsletterFollowers
)

from .forms import (
	PublicBlogForm)

from .utils import get_or_create_follower

User = get_user_model()


def writter_profile_view(request, host_name):
	template_name = 'profile/public/profile.html'
	context = {}
	context['current_profile'] = WritterProfile.objects.get(host_name = host_name).user

	return render(request, template_name, context)


def following_management_view(request):
	if request.POST:
		email = request.POST['email'] 
		writter = request.POST['writter']
		action = request.POST['what']

		writter = User.objects.get(id = writter)
	
		follower = get_or_create_follower(email, request)
		
		update_follower = writter.update_followers(follower, action)

		if update_follower == 'already follower':
			messages.success(request, f'Ya estás siguiendo a {writter.full_name}')
			return redirect(request.META.get('HTTP_REFERER'))

		messages.success(request, f'A partir de ahora recibirás las newsletters de {writter.full_name}')
		return redirect(request.META.get('HTTP_REFERER'))


@login_required
def user_become_writter_view(request):
	if request.method == 'POST':
		domain = request.POST['domain'].lower()
		WritterProfile.objects.create(user = request.user, host_name = domain)
		request.user.is_writter = True
		request.user.save()
		NewsletterFollowers.objects.create(user = request.user)
		messages.success(request, f'Pon al día tu perfil, \
				añade tus redes sociales, una buena descripción y tu nombre para que la gente pueda conocerte.')
		return redirect('users:update')


class PublicBlogsListView(ListView):
	model = PublicBlog
	template_name = 'public_blog/inicio.html'
	ordering = ['-published_at']
	context_object_name = "blogs"

	def get_queryset(self):
		queryset = PublicBlog.objects.filter(status = 1)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['escritores'] = WritterProfile.objects.all()
		context["meta_desc"] = 'El blog donde tu también puedes escribir de forma libre'
		context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir'
		context["meta_title"] = 'Convíertete en escritor'
		context["meta_url"] = '/blog-financiero/'
		return context


class PublicBlogDetailsView(DetailView):
	model = PublicBlog
	template_name = 'public_blog/details.html'
	context_object_name = "object"
	slug_field = 'slug'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		model = self.get_object()
		model.total_views += 1
		model.save()
		return context


class WritterOnlyView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin):
    def test_func(self):
        valid = False
        if self.request.user.is_writter:
            valid = True
        return valid

    def handle_no_permission(self):
        return redirect("public_blog:blog_list")


class WritterOwnBlogsListView(WritterOnlyView, DetailView):
	model = User
	template_name = 'public_blog/profile/manage_blogs.html'
	ordering = ['-published_at']
	slug_field = 'username'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		writter = self.get_object()
		context["newsletter_fields_form"] = DefaultNewsletterFieldsForm()
		context["blogs"] = PublicBlog.objects.filter(author = writter)
		context["meta_desc"] = 'El blog donde tu también puedes escribir de forma libre'
		context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir'
		context["meta_title"] = 'Dashboard'
		context["meta_url"] = f'management/escritos/{writter.username}/'
		return context


class UpdatePublicBlogPostView(WritterOnlyView, UpdateView):
	model = PublicBlog
	form_class = PublicBlogForm
	context_object_name = "public_blog_form"
	success_message = 'Escrito actualizado'
	template_name = 'public_blog/forms/update.html'

	def get_context_data(self, **kwargs):
		context = super(UpdatePublicBlogPostView, self).get_context_data(**kwargs)        
		context['current_tags'] = self.get_object().tags.all()
		return context

	def form_valid(self, form):
		return super(UpdatePublicBlogPostView, self).form_valid(form)

	def test_func(self):
		valid = False
		if self.get_object().author == self.request.user:
			valid = True
		return valid


class CreatePublicBlogPostView(WritterOnlyView, CreateView):
	model = PublicBlog
	form_class = PublicBlogForm
	success_message = 'Escrito creado'
	template_name = 'public_blog/forms/create.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		tags = self.request.POST['tags'].split(',')		
		modelo = form.save()
		modelo.add_tags(tags)
		modelo.save_secondary_info('blog')
		return super(CreatePublicBlogPostView, self).form_valid(form)


class CreateBlogNewsletterView(BaseNewsletterView, CreateView):
	model = PublicBlog
	context_object_name = "newsletter_form"
	success_message = 'Escrito actualizado'
	template_name = 'public_blog/forms/update.html'

	def test_func(self):
		valid = False
		if self.get_object().author == self.request.user:
			valid = True
		return valid
    

class UpdateBlogNewsletterView(BaseNewsletterView, UpdateView):
	model = PublicBlogAsNewsletter
	context_object_name = "newsletter_form"
	success_message = 'Escrito actualizado'
	template_name = 'public_blog/forms/update.html'

	def test_func(self):
		valid = False
		if self.get_object().blog_related.author == self.request.user:
			valid = True
		return valid