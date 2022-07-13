from rest_framework.serializers import FloatField, ModelSerializer, StringRelatedField


class ExchangeOrganisationSerializer(ModelSerializer):

    class Meta:
        model = ExchangeOrganisation
        exclude = ['id']
