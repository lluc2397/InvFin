from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)

from ..models import Superinvestor, SuperinvestorActivity, SuperinvestorHistory


class SuperinvestorSerializer(ModelSerializer):
    class Meta:
        model = Superinvestor
        exclude = [
            'id',
            'fund_name',
            'last_update',
            'has_error',
            'error',
            'image',
        ]


class BaseSuperinvestorInfo(ModelSerializer):
    superinversor = StringRelatedField(many=False, source='superinvestor_related')
    empresa = StringRelatedField(many=False, source='company')
    periodo = StringRelatedField(source='period_related')
    nombre_empresa = SerializerMethodField()

    class Meta:
        exclude = [
            'id',
            'not_registered_company',
            'need_verify_company',
            'superinvestor_related',
            'company',
            'period_related',
            'company_name'
        ]
    
    def get_nombre_empresa(self, obj):
        return obj.actual_company_info['full_name']


class SuperinvestorActivitySerializer(BaseSuperinvestorInfo):
    movimiento = SerializerMethodField(source='movement')

    class Meta(BaseSuperinvestorInfo.Meta):
        model = SuperinvestorActivity
        exclude = BaseSuperinvestorInfo.Meta.exclude + ['movement'] 
    
    def get_movimiento(self, obj):
        return obj.movement_type['move']


class SuperinvestorHistorySerializer(BaseSuperinvestorInfo):
    class Meta(BaseSuperinvestorInfo.Meta):
        model = SuperinvestorHistory