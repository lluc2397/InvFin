from typing import Dict, List, Union

from django.db.models import QuerySet, Model
from django.views.generic import TemplateView
from django.apps import apps

from apps.empresas.models import Company, Exchange
from apps.escritos.models import Term
from apps.general.models import Country, Industry, Sector
from apps.public_blog.models import PublicBlog
from apps.seo import constants
from apps.seo.models import Visiteur
from apps.users.models import User

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
    model_to_recommend = None
    place = None
    location = None
    kind = None
    recommendation_log_model = None

    def get_recommendation_log_model(self) -> Model:
        if not self.recommendation_log_model:
            model_to_recommend_name = self.model_to_recommend.object_name
            user = "User"
            if self.request.is_visiteur:
                user = "Visiteur"
            object_name = f"{user}{model_to_recommend_name}Recommended"
            return apps.get_model("recsys", object_name, require_ready=True)
        return self.recommendation_log_model
    
    def save_recommendations(
        self, 
        recommendations: Union[QuerySet, List],
        recommendation_explained: Dict
    ) -> None:
        recommendation_log_model = self.get_recommendation_log_model()
        user = self.request.visiteur if self.request.is_visiteur else self.request.user
        for recommendation in recommendations:
            recommendation_log_model.objects.create(
                user=user,
                place=self.place,
                location=self.location,
                kind=self.kind,
                recommendation_explained=recommendation_explained,
                model_recommended=recommendation
            )
    
    def return_recommendations(self, recommendations: Union[QuerySet, List], slice_recommedations: int = None):
        if slice_recommedations:
            final_recommendations = recommendations[:slice_recommedations]
        
        self.save_recommendations(final_recommendations, recommendation_explained)
        return final_recommendations
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommendations'] = self.return_recommendations()
        return context


class BaseCompanyRecommendationView(BaseRecommendationView):
    model_to_recommend = Company
    place = None
    location = None
    kind = None

    def get_specific_company_recommendations(self, companies_visited) -> QuerySet:
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
    
    def get_random_companies_recommendations(self) -> QuerySet:
        return Company.objects.related_companies()
    
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


class CompaniesRecommendedSide(BaseCompanyRecommendationView):
    template_name = 'side_recsys.html'
    place = constants.SIDE
    location = constants.ALL_WEB
    kind = constants.LISTA

    