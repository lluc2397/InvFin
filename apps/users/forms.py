from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import (
    Profile,
    MetaProfileHistorial,
    MetaProfile
    )

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserSignupForm(SignupForm):
    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.create_new_user(request)
        
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username'
        ]


class UserProfileForm(forms.ModelForm):
    edad= forms.DateField(widget=forms.SelectDateWidget)

    new_blog_post = forms.BooleanField(required=False, label='Nueva publicación de mis escritores favoritos')
    new_comment = forms.BooleanField(required=False, label='Nuevo comentario en mi publicación')
    new_vote = forms.BooleanField(required=False, label='Nuevo voto en mi publicación')
    new_follower = forms.BooleanField(required=False, label='Nuevo seguidor')
    new_question = forms.BooleanField(required=False, label='Nueva pregunta')
    new_answer = forms.BooleanField(required=False, label='Nueva respuesta en mi publicación')
    answer_accepted = forms.BooleanField(required=False, label='Respuesta acceptada')
    new_obs_company = forms.BooleanField(required=False, label='Nuevo análisis para mis empresas favoritas')
    new_news_company = forms.BooleanField(required=False, label='Nuevas noticias para mis empresas favoritas')

    class Meta:
        model = Profile
        fields = [
            'edad',
            'ciudad',
            'pais',
            'foto_perfil',
            'bio',
            'new_blog_post',
            'new_comment',
            'new_vote',
            'new_follower',
            'new_question',
            'new_answer',
            'answer_accepted',
            'new_obs_company',
            'new_news_company',
        ]
