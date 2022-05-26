from rest_framework.serializers import (
    StringRelatedField,
    ModelSerializer,
    CharField,
    IntegerField
)

from ..models import Term, TermContent

class TermSerializer(ModelSerializer):
    titulo = CharField(source='title')
    slug = CharField(source='slug')
    resumen = CharField(source='resume')
    votos_totales = IntegerField(source='total_votes')
    visitas_totales = IntegerField(source='total_views')
    veces_compartido = IntegerField(source='times_shared')
    categoría = StringRelatedField(source='category')
    autor = StringRelatedField(source='author')
    imagen = CharField(source='image')

    class Meta:
        model = Term
        fields = [
            'id',
            'titulo',
            'slug',
            'resumen',
            'votos_totales',
            'visitas_totales',
            'veces_compartido',
            'categoría',
            'autor',
            'imagen',
        ]


class TermContentSerializer(ModelSerializer):
    titulo = CharField(source='title')
    orden = CharField(source='order')
    contenido = CharField(source='content')

    class Meta:
        model = TermContent
        fields = [
            'id',
            'titulo',
            'orden',
            'contenido',
        ]
