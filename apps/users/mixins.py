from django.contrib.auth.models import AbstractUser



class UserBaseMixin(AbstractUser):
    class Meta:
        abstract = True


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
        self.create_profile(request)
        self.create_meta_profile(request)
        self.add_fav_lists()
        return True