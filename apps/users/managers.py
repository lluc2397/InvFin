import secrets
import string
import uuid

from django.contrib.auth import login, models
from django.db.models import Manager, Model

from .constants import ADD, REDUCE


class UserExtraManager(models.BaseUserManager):
    
    def get_or_create_quick_user(
        self, 
        request, 
        email: str = None, 
        just_newsletter:bool=False, 
        just_correction:bool=False, 
        local_request:bool=True
    ):
        if request.user.is_authenticated:
            user = request.user
        else:
            if request.POST:
                email_request = request.POST.get('email', None)
                if email_request and not email:
                    email = email_request
            if self.filter(email = email).exists():
                user = self.get(email = email)

            else:
                user = self.create(
                username = email.split('@')[0],
                email = email,
                password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20))),
                just_newsletter = just_newsletter,
                just_correction = just_correction)
                
                if local_request:
                    user.create_new_user(request)
                    request.session['F-E'] = email
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return user


class ProfileManager(Manager):
    
    def create_ref_code(self) -> uuid:
        ref_code = str(uuid.uuid4())[:100]
        if self.filter(ref_code = ref_code).exists():
            return self.create_ref_code()
        else:
            return ref_code
    

class CreditHistorialManager(Manager):

    def check_enought_credits(self, user: Model, amount: int) -> bool:
        return bool(user.user_profile.creditos >= amount)
    
    def update_credits(
        self, 
        user: Model,
        amount: int, 
        move_source: str, 
        movement: int = ADD, 
        extra_objects: Model = None):

        enought_credits = True
        if movement == REDUCE:
            enought_credits = self.check_enought_credits(user, amount)
            amount = -amount
        
        final = user.user_profile.creditos + amount
        creadits_transaction = {
            'user': user,
            'amount': amount,
            'movement': movement,
            'move_source': move_source,
            'initial': user.user_profile.creditos,
            'final': final,
            'has_enought_credits': enought_credits
        }
        if extra_objects:
            creadits_transaction['object'] = extra_objects
        self.create(**creadits_transaction)
        if enought_credits is False:
            return f"No tienes bastantes créditos, todavía te faltan {final}"
        user.update_credits(amount)


