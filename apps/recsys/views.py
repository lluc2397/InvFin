from django.views.generic import TemplateView

from apps.empresas.models import Company, Exchange
from apps.escritos.models import Term
from apps.general.models import Country, Industry, Sector
from apps.public_blog.models import PublicBlog
from apps.seo import constants


class ExplorationView(TemplateView):
    template_name = 'escritos/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['terms'] = Term.objects.filter(status = 1)
        context['blogs'] = PublicBlog.objects.filter(status = 1)
        context['companies'] = Company.objects.get_companies_user_likes(self.reqeust.user)
        return context


class RecsysViewMixin:
    num_companies = None



# Hacer vistas para mostrar recomendaciones de terms, comps, etc... 
# despues crear api views para que si el usuario tiene algo para recomendarle
# mostrarselo.
# Hay que hacer un algoritmo que busque en el seo journey las búsquedas y las empareje con los usuarios.
# Despues hay que recomendar en diferentes partes de la web cosas que puedan gustarle al usuario.
# Si no le gusta restar un punto. Si le gusta sumar un punto. Ir guardando los gustos para mejorar las recomendaciones
# Preparar banners, listas y Call To action
# Añadir empresas, terms, preguntas en los sides de los términos, preguntas, blogs


class BaseRecommendationView(TemplateView):
    model = None
    place = None
    rec_type = None

class CompaniesRecommendedSide(BaseRecommendationView):
    template_name = 'recsys/side.html'
    model = Company
    place = constants.SIDE
    rec_type = constants.LISTA

    def get_specific_company_recommendations(self, companies_visited):
        unique_sectors_id = set()
        unique_industries_id = set()
        unique_countries_id = set()
        unique_exchanges_id = set()
        for company in companies_visited:
            unique_sectors_id.add(company['sector_id'])
            unique_industries_id.add(company['industry_id'])
            unique_countries_id.add(company['country_id'])
            unique_exchanges_id.add(company['exchange_id'])
        
        unique_sectors_id = list(unique_sectors_id)
        unique_industries_id = list(unique_industries_id)
        unique_countries_id = list(unique_countries_id)
        unique_exchanges_id = list(unique_exchanges_id)

        sectors = Sector.objects.filter(id__in=unique_sectors_id)
        industries = Industry.objects.filter(id__in=unique_industries_id)
        countries = Country.objects.filter(id__in=unique_countries_id)
        exchanges = Exchange.objects.filter(id__in=unique_exchanges_id)
        return Company.objects.related_companies(
            sectors,
            industries,
            countries,
            exchanges,
        )
    
    def get_random_companies_recommendations(self):
        return Company.objects.related_companies()
    
    def save_recommendations(self, recommendations):
        for recommendation in recommendations:
            user
            place
            kind
            clicked
            recommendation_personalized
            recommendation_explained


    def get_companies_to_recommend(self):
        companies_visited = self.get_companies_visited()
        if companies_visited:
            recommendations =  self.get_specific_company_recommendations(companies_visited)
        else:
            recommendations = self.get_random_companies_recommendations()
        self.save_recommendations(recommendations)
        return recommendations
            
    def get_companies_visited(self):
        if 'companies_visited' in self.request.session:
            companies_visited = self.request.session['companies_visited']
            for company_visited in companies_visited:
                if not 'sector_id' in company_visited:
                    company = Company.objects.get(ticker=company_visited['ticker'])
                    company_visited.update(
                        {
                            'ticker': company.ticker, 
                            'img': company.image,
                            "sector_id": company.sector.id,
                            "industry_id": company.industry.id,
                            "country_id": company.country.id,
                            "exchange_id": company.exchange.id,
                        }
                    )
                    self.request.session.modified = True
            return companies_visited

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = self.get_companies_to_recommend()[:5]
        return context