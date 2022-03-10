from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DetailView, 
    RedirectView, 
    UpdateView, 
    TemplateView)

from apps.public_blog.forms import WritterProfileForm
from apps.public_blog.models import WritterProfile

from .forms import UserForm, UserProfileForm
from .models import Profile
User = get_user_model()


class UserDetailView(LoginRequiredMixin, TemplateView):

    template_name = 'profile/private/inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["meta_desc"] = 'Todo lo que necesitas para invertir'
        context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir'
        context["meta_title"] = 'Dashboard'
        context["meta_url"] = '/inicio/'
        return context


class UserPublicProfileDetailView(DetailView):

    template_name = 'profile/public/profile.html'
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "current_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def user_update_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.user_profile)
        form = UserForm(request.POST, instance=request.user)

        if request.user.is_writter:
            writter_form = WritterProfileForm(request.POST, instance=request.user.writter_profile)

        vieja_foto = request.user.user_profile.foto_perfil

        if profile_form.is_valid() and form.is_valid():
            
            if request.user.is_writter:
                if writter_form.is_valid():
                    writter_form.save()

            new_profile = profile_form.save(commit=False)
            new_foto = new_profile.foto_perfil
            if new_foto != vieja_foto:
                new_profile.transform_photo(new_foto)
                   
            new_profile.save()
            
            form.save()
            messages.success(request, f'Perfil actualizado.')
            return redirect('users:update')

    else:
        form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.user_profile)
        writter_form = WritterProfileForm(instance=request.user.writter_profile)
   
    return render(request, 'profile/private/settings.html', {'profile_form': profile_form, 'form': form, 'writter_form':writter_form})


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("preguntas_respuestas:list_questions")
