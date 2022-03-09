import secrets
import string

from django.contrib.auth import get_user_model
User = get_user_model()


def get_or_create_follower(email, request):  
    if User.objects.filter(email = email).exists():
        follower = User.objects.get(email = email)

    else:
        follower = User.objects.create(
        username = email.split('@')[0],
        email = email,
        password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20))),
        just_newsletter = True)
        follower.create_meta_profile(request)
        request.session['F-E'] = email

    return follower