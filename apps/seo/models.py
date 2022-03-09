from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    CASCADE,
    ForeignKey,
    TextField,
    DateTimeField,
    BooleanField,
    IntegerField,
    PositiveBigIntegerField,
    JSONField
)

from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()


class Visiteur(Model):
    ip = CharField(max_length=10000, null=True, blank=True)
    session_id = CharField(max_length=10000, null=True, blank=True)
    HTTP_USER_AGENT = CharField(max_length=10000, null=True, blank=True)
    country_code = CharField(max_length=10000, null=True, blank=True)
    country_name = CharField(max_length=10000, null=True, blank=True)
    dma_code = CharField(max_length=10000, null=True, blank=True)
    is_in_european_union = BooleanField(null=True, blank=True)
    latitude = CharField(max_length=10000, null=True, blank=True)
    longitude = CharField(max_length=10000, null=True, blank=True)
    city = CharField(max_length=10000, null=True, blank=True)
    region = CharField(max_length=10000, null=True, blank=True)
    time_zone = CharField(max_length=10000, null=True, blank=True)
    postal_code = CharField(max_length=10000, null=True, blank=True)
    continent_code = CharField(max_length=10000, null=True, blank=True)
    continent_name = CharField(max_length=10000, null=True, blank=True)
    first_visit_date = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Visiteur"
        db_table = "visiteurs"
    

class MetaParameters(Model):
    meta_title = CharField(max_length=99999,null=True, blank=True)
    meta_description = TextField(null=True, blank=True)
    meta_img = CharField(max_length=99999,null=True, blank=True)
    meta_url = CharField(max_length=99999,null=True, blank=True)
    meta_keywords = TextField()
    meta_author = ForeignKey(User, on_delete=SET_NULL, null=True)
    published_time = DateTimeField(auto_now=True)
    modified_time = DateTimeField(auto_now=True)
    created_at = DateTimeField(default=timezone.now)    
    views = PositiveBigIntegerField(default=0)
    schema_org = JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Meta information"
        db_table = "meta_information"

    def __str__(self):
        return self.meta_title


class MetaParametersHistorial(Model):
    parameter_settings = ForeignKey(MetaParameters, on_delete= CASCADE, null=True)
    in_use = BooleanField(default=True)

    class Meta:
        verbose_name = "Historial meta información"
        db_table = "meta_information_historial"

    def __str__(self):
        return self.parameter_settings.meta_title


class Journey(Model):
    date = DateTimeField(auto_now_add=True)
    current_path = CharField(max_length=20000, null=True, blank=True)
    comes_from = CharField(max_length=20000, null=True, blank=True)

    class Meta:
        abstract = True


class VisiteurJourney(Journey):
    user = ForeignKey(Visiteur, null = True, blank=True, on_delete=CASCADE)

    class Meta:
        verbose_name = "Historial visitas anónimos"
        db_table = "visits_historial_visiteurs"
    

class UsersJourney(Journey):
    user = ForeignKey(User, null = True, blank=True, on_delete=CASCADE)

    class Meta:
        verbose_name = "Historial visitas usuarios"
        db_table = "visits_historial_users"
    
