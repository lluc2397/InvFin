from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Key


class ReadOnly(BasePermission):
    message = 'Solamente se puede leer, ingresa en tu perfil si quieres hacer una corrección'

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CheckCuota(BasePermission):
    message = 'Ya has usado toda tu cuota, si quieres aumentarla puedes pedirlo desde tu perfil'

    def has_permission(self, request, view):
        key = request.GET.get('api_key')
        if key:
            return Key.objects.has_cuota(key)
        raise AuthenticationFailed(
            'Introduce tu clave en api_key, si no tienes alguna entra en tu perfil para crearla'
        )