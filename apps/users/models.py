from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,
    Model,
    OneToOneField,
    BooleanField,
    SET_NULL,
    CASCADE,
    ForeignKey,
    ImageField,
    IntegerField,
    DateTimeField,
    DateField,
    TextField
    
    )
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from django_countries.fields import CountryField
from cloudinary.models import CloudinaryField

from apps.general.mixins import ResizeImageMixin
from .manager import ProfileManager, UserExtraManager


class User(AbstractUser):
    first_name = CharField(_("Nombre"), blank=True, max_length=2550)
    last_name = CharField(_("Apellidos"), blank=True, max_length=2550)
    is_writter = BooleanField(default=False)
    just_newsletter = BooleanField(default=False)
    just_correction = BooleanField(default=False)
    objects = UserExtraManager()

    class Meta:
        db_table = "users"
        ordering = ['-date_joined']
    
    def __str__(self) -> str:
        return self.full_name

    def get_absolute_url(self):
        return reverse("users:user_public_profile", kwargs={"username": self.username})

    @property
    def custom_url(self):
        url = self.get_absolute_url()
        if self.is_writter:
            host_name = self.writter_profile.host_name
            domain = Site.objects.get_current().domain
            url = f'https://{host_name}.{domain}'
        return url
    
    @property
    def foto(self):
        return self.user_profile.foto_perfil.url
    
    @property
    def full_name(self):
        if self.first_name:
            full_name = self.first_name
        if self.first_name and self.last_name:
            full_name = f'{self.first_name} {self.last_name}'
        else:
            full_name = self.username
        return full_name
    
    @property
    def questions_asked(self):
        return self.question_set.all()
    
    @property
    def answers_apported(self):
        return self.question_set.all()
    
    @property
    def answers_accepted(self):
        return self.answers_apported.filter(is_accepted = True)

    @property
    def number_of_questions(self):
        return self.questions_asked.count()

    @property
    def number_of_answers(self):
        return self.answers_apported.count()

    @property
    def number_of_accepted_answers(self):
        return self.answers_accepted.count()
    
    @property
    def number_of_contributions(self):
        return (
            self.number_of_questions
            + self.number_of_answers)
    
    @property
    def blogs_written(self):
        if self.is_writter:
            return self.publicblog_set.filter(status = 1)
        return []
    
    @property
    def fav_stocks(self):
        fav_stocks = self.favorites_companies.stock.all()
        return fav_stocks
    
    @property
    def fav_terms(self):
        fav_terms = self.favorites_terms.term.all()        
        return fav_terms
    
    @property
    def fav_writters(self):
        from apps.public_blog.models import NewsletterFollowers
        fav_writters = NewsletterFollowers.objects.filter(followers = self)
        if fav_writters.count() !=0:
            return [writter.user for writter in fav_writters]
        return []
    
    def add_credits(self, number_of_credits):
        self.user_profile.creditos += number_of_credits
        self.user_profile.save()


    def update_followers(self, user, action):
        from apps.public_blog.models import FollowingHistorial
        if self.is_writter:
            following_historial = FollowingHistorial.objects.create(user_followed = self, user_following = user)
            writter_followers = self.main_writter_followed
            if action == 'stop':
                following_historial.stop_following = True
                writter_followers.followers.remove(user)
            elif action == 'start':
                if user in writter_followers.followers.all():
                    return 'already follower'
                following_historial.started_following = True
                writter_followers.followers.add(user)
                #enviar email para avisar que tiene un nuevo seguidor
            
            following_historial.save()
            writter_followers.save()
            
            return True
            
    
    def update_reputation(self, points):
        self.user_profile.reputation_score += points
        self.user_profile.save()


    def create_meta_profile(self, request):
        from .models import MetaProfile
        from apps.seo.utils import SeoInformation
        seo = SeoInformation().meta_information(request)
        meta_profile = MetaProfile.objects.create(
            ip = seo['ip'],
            country_code = seo['location']['country_code'],
            country_name = seo['location']['country_name'],
            dma_code = seo['location']['dma_code'],
            is_in_european_union = seo['location']['is_in_european_union'],
            latitude = seo['location']['latitude'],
            longitude = seo['location']['longitude'],
            city = seo['location']['city'],
            region = seo['location']['region'],
            time_zone = seo['location']['time_zone'],
            postal_code = seo['location']['postal_code'],
            continent_code = seo['location']['continent_code'],
            continent_name = seo['location']['continent_name'],
            user_agent = seo['http_user_agent']    
        )
        
        self.meta_profile.model.objects.create(
            meta_info = meta_profile
        )
        return True


    def create_profile(self, request):
        from .models import Profile
        user_profile = Profile.objects.create(user = self)
        user_recomending_id = request.session.get('recommender')
        if user_recomending_id is not None:
            recommended_by_user = self.__class__.objects.get(id=user_recomending_id)
            user_profile.recommended_by = recommended_by_user
            user_profile.save()
        return True


    def add_fav_lists(self):
        from apps.escritos.models import FavoritesTermsList
        from apps.screener.models import FavoritesStocksList

        FavoritesTermsList.objects.create(user = self)
        FavoritesStocksList.objects.create(user = self)

        
    def create_new_user(self, request):
        from allauth.account.utils import sync_user_email_addresses

        sync_user_email_addresses(self)
        self.create_profile(request)
        self.create_meta_profile(request)
        self.add_fav_lists()
        return True


class MetaProfile(Model):    
    ip = CharField(max_length=10000, null=True, blank=True)
    country_code = CharField(max_length=10000, null=True, blank=True)
    country_name = CharField(max_length=10000, null=True, blank=True)
    dma_code = CharField(max_length=10000, null=True, blank=True)
    is_in_european_union = BooleanField(default=False)
    latitude = CharField(max_length=10000, null=True, blank=True)
    longitude = CharField(max_length=10000, null=True, blank=True)
    city = CharField(max_length=10000, null=True, blank=True)
    region = CharField(max_length=10000, null=True, blank=True)
    time_zone = CharField(max_length=10000, null=True, blank=True)
    postal_code = CharField(max_length=10000, null=True, blank=True)
    continent_code = CharField(max_length=10000, null=True, blank=True)
    continent_name = CharField(max_length=10000, null=True, blank=True)
    user_agent = CharField(max_length=10000, null=True, blank=True)

    class Meta:
        verbose_name = "Meta profile info"
        db_table = "meta_profile_info"


class MetaProfileHistorial(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, related_name='meta_profile')
    date = DateTimeField(auto_now_add=True)
    meta_info = ForeignKey(MetaProfile, blank=True, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Meta profile historial"
        db_table = "meta_profile_historial"


class Profile(Model, ResizeImageMixin):
    user = OneToOneField(User, on_delete=CASCADE, null=True, related_name='user_profile')
    reputation_score = IntegerField(default=0)
    creditos = IntegerField(default=0)
    edad = DateField("Fecha de nacimiento (DD/MM/AAAA)", null=True, blank=True)
    pais = CountryField("País de origen", null=True, blank=True, blank_label='(select country)')
    ciudad = CharField("Ciudad de origen", max_length=150,null=True, blank=True)
    # foto_perfil = CloudinaryField("Foto de perfil", 'image', null=True, width_field='image_width', height_field='image_height', default="inversorinteligente.png")
    foto_perfil = ImageField("Foto de perfil", upload_to='avatar/', default="inversorinteligente.WebP")
    bio = TextField("Descripción", null=True, blank=True)
    recommended_by = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='invited_by') 
    ref_code = CharField(max_length=1000, blank=True, unique=True)
    objects = ProfileManager()

    class Meta:
        verbose_name = "Users profile"
        db_table = "profiles"
    
    def __str__(self) -> str:
        return self.user.full_name
    
    def save(self, *args, **kwargs):
        if self.ref_code == "":
            self.ref_code = Profile.objects.create_ref_code()
        super().save(*args, **kwargs)
    
    def transform_photo(self, img):
        self.resize(img, (400, 400))
        self.save()