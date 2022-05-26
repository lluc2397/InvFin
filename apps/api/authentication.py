from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import Key


class KeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.GET.get('api_key')
        if key:
            if Key.objects.filter(key=key).exists() is True:                
                if Key.objects.key_is_active(key) is True:
                    return (Key.objects.get_key(key), None)

                key = Key.objects.filter(key=key).first()
                raise AuthenticationFailed(
                    f'Tu clave ya no es válida desde el {key.removed}, cera una nueva desde tu perfil'
                )
            raise AuthenticationFailed(
                'Tu clave es incorrecta, asegúrate que está bien escrita o pide tu clave desde tu perfil'
            )
        raise AuthenticationFailed(
            'Introduce tu clave en api_key, si no tienes alguna entra en tu perfil para crearla'
        )
