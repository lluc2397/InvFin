from django.shortcuts import render
from django.views.generic import TemplateView

from apps.public_blog.models import PublicBlog
from apps.escritos.models import Term
from apps.empresas.models import Company


class ExplorationView(TemplateView):
    template_name = 'escritos/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['terms'] = Term.objects.filter(status = 1)
        context['blogs'] = PublicBlog.objects.filter(status = 1)
        return context

# Hacer vistas para mostrar recomendaciones de terms, comps, etc... 
# despues crear api views para que si el usuario tiene algo para recomendarle
# mostrarselo.
# Hay que hacer un algoritmo que busque en el seo journey las búsquedas y las empareje con los usuarios.
# Despues hay que recomendar en diferentes partes de la web cosas que puedan gustarle al usuario.
# Si no le gusta restar un punto. Si le gusta sumar un punto. Ir guardando los gustos para mejorar las recomendaciones
# Preparar banners, listas y Call To action