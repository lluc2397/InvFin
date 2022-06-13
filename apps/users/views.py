from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DetailView,
    TemplateView)

from apps.public_blog.forms import WritterProfileForm

from .forms import UserForm, UserProfileForm
from .models import Profile

from itertools import chain

User = get_user_model()


class UserDetailView(LoginRequiredMixin, TemplateView):

    template_name = 'profile/private/inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_desc"] = 'Todo lo que necesitas para invertir'
        context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir'
        context["meta_title"] = f'Bienvenido {self.request.user.username}'
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
        user = self.get_object()
        context["meta_desc"] = user.user_profile.bio
        context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir, excel'
        context["meta_title"] = user.username
        context["meta_url"] = f'perfil/{user.username}/'
        return context


def invitation_view(request, invitation_code):
    perfil = Profile.objects.get(ref_code = invitation_code)        
    request.session['recommender'] = perfil.id
    context = {
        'meta_desc': 'Todo lo que necesitas para invertir',
        'meta_tags': 'finanzas, blog financiero, blog el financiera, invertir',
        'meta_title': 'Dashboard',
        'meta_url': '/inicio/',
    }
    return redirect('account_signup') 


@login_required
def user_update_profile(request):
    writter_profile = None
    if request.user.is_writter:
        writter_profile = request.user.writter_profile
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.user_profile)
        form = UserForm(request.POST, instance=request.user)

        if request.user.is_writter:
            writter_form = WritterProfileForm(request.POST, instance=writter_profile)

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
        writter_form = WritterProfileForm(instance=writter_profile)

        context = {
            'profile_form': profile_form, 
            'form': form, 
            'writter_form':writter_form,
            
            'meta_title': 'Tu perfil',
            
            }
   
    return render(request, 'profile/private/settings.html', context)


class UserHistorialView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/private/historial.html'

    def meta_information(self, slug):
        return {
            "meta_desc": 'Tu historial en la plataforma',
            "meta_tags": 'finanzas, blog financiero, blog el financiera, invertir',
            "meta_title": f'Historial de {slug}',
            "meta_url": f'/historial-perfil/{slug}'
        }
    
    def get_object(self, slug):
        user = self.request.user
        if slug == 'Aportes':
            content = user.corrector.all()
            url = 'escritos:glosario'
        elif slug == 'Comentarios':
            questions_coms = user.quesitoncomment_set.all()
            answers_coms = user.answercomment_set.all()
            content = list(chain(answers_coms, questions_coms))
            url = 'preguntas_respuestas:list_questions'
        else:
            content = user.usercompanyobservation_set.all()
            url = 'screener:screener_inicio'
        return {
            'content': content,
            'slug': slug,
            'url': reverse(url)
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context.update(self.meta_information(slug))
        if self.request.user.is_authenticated:
            context.update(self.get_object(slug))        
        return context