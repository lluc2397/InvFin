from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.sessions.models import Session

from apps.seo.models import Visiteur


def generate_utm_url(
        utm_source: str,
        utm_medium: str,
        utm_campaign: str,
        utm_term: str,
        link: str = None
    ) -> str:
        utm_source = f'utm_source={utm_source}'
        utm_medium = f'utm_medium={utm_medium}'
        utm_campaign = f'utm_campaign={utm_campaign}'
        utm_term = f'utm_term={utm_term}'
        utm_params = f'{utm_source}&{utm_medium}&{utm_campaign}&{utm_term}'
        if link:
            return f'{link}?{utm_params}'
        return utm_params


class SeoInformation:
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            
            ip = x_forwarded_for.split(',')[-1].strip()
        elif request.META.get('HTTP_X_REAL_IP'):
            
            ip = request.META.get('HTTP_X_REAL_IP')
        else:
            
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def meta_information(self, request):
        g = GeoIP2()
        ip = self.get_client_ip(request)
        if settings.DEBUG:
            ip = '162.158.50.77'
        meta = {
            'http_user_agent' : request.META.get("HTTP_USER_AGENT"),
            'location':g.city(ip),
            'ip':ip
        }
        
        return meta

    def update_visiteur_session(self, visiteur, request):
        if not request.session or not request.session.session_key:
            request.session.save()
        visiteur.session_id = request.session.session_key
        visiteur.save(update_fields=['session_id'])
        request.session['visiteur_id'] = visiteur.id
        request.session.modified = True
        return visiteur

    def get_visiteur_by_old_session(self, request):
        session = Session.objects.filter(session_key = request.session.session_key)
        visiteur = False
        if session.exists():
            session_obj = Session.objects.get(session_key = request.session.session_key)
            session_obj_visiteur_id = session_obj.get_decoded().get("visiteur_id")
            if session_obj_visiteur_id:
                visiteur = Visiteur.objects.get(id = session_obj_visiteur_id)
        return visiteur

    def find_visiteur(self, request):
        seo = self.meta_information(request)
        visiteur = self.get_visiteur_by_old_session(request)
        if visiteur == False:
            find_visiteur = Visiteur.objects.filter(ip = seo['ip'])
            if find_visiteur.exists():
                if find_visiteur.count() != 1:
                    second_filter = find_visiteur.filter(HTTP_USER_AGENT = seo['http_user_agent'])
                    if second_filter.exists():
                        if second_filter.count() != 1:
                            visiteur = self.create_visiteur(request)
                        else:
                            visiteur = Visiteur.objects.get(ip = seo['ip'], HTTP_USER_AGENT = seo['http_user_agent'])
                            self.update_visiteur_session(visiteur, request)
                    else:
                        visiteur = self.create_visiteur(request)
                else:
                    visiteur = Visiteur.objects.get(ip = seo['ip'])
                    self.update_visiteur_session(visiteur, request)
            else:
                visiteur = self.create_visiteur(request)
        return visiteur
    
    def create_visiteur(self, request):
        seo = self.meta_information(request)
        if not request.session or not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        visiteur = Visiteur.objects.create(
            ip = seo['ip'],
            session_id = session_id,
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
            HTTP_USER_AGENT = seo['http_user_agent']
        )
        request.session['visiteur_id'] = visiteur.id
        request.session.modified = True
        return visiteur
