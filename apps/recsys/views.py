from typing import Dict, List, Union

from django.db.models import QuerySet, Model
from django.views.generic import TemplateView, RedirectView
from django.apps import apps

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


class RecommendationClickedRedirectView(RedirectView):
    def get_and_save_model(self):
        pk = self.kwargs['pk']
        object_name = self.kwargs['object_name']
        obj = apps.get_model("recsys", object_name, require_ready=True).objects.get(id=pk)
        obj.clicked = True
        obj.save(update_fields=['clicked'])
        return obj
    
    def generate_url(
        self,
        obj: Model,
        medium: str='webapp',
        source: str='invfin',
        campaign:str='recsys'
        ):
        content=obj.location
        term=obj.model_recommended
        place=obj.place
        kind=obj.kind
        utm_source = f'utm_source={source}'
        utm_medium = f'utm_medium={medium}'
        utm_campaign = f'utm_campaign={campaign}'
        utm_content = f'utm_content={content}'
        utm_term = f'utm_term={term}'
        return f'?{utm_source}&{utm_medium}&{utm_content}&{utm_campaign}&{utm_term}&{place}&{kind}'

    def get_redirect_url(self, *args, **kwargs):
        obj = self.get_and_save_model()
        path_params = self.generate_url(obj)
        path = obj.model_recommended.get_absolute_url()
        return f"{path}{path_params}"

# Hacer vistas para mostrar recomendaciones de terms, comps, etc... 
# despues crear api views para que si el usuario tiene algo para recomendarle
# mostrarselo.
# Hay que hacer un algoritmo que busque en el seo journey las búsquedas y las empareje con los usuarios.
# Despues hay que recomendar en diferentes partes de la web cosas que puedan gustarle al usuario.
# Si no le gusta restar un punto. Si le gusta sumar un punto. Ir guardando los gustos para mejorar las recomendaciones
# Preparar banners, listas y Call To action
# Añadir empresas, terms, preguntas en los sides de los términos, preguntas, blogs


class BaseRecommendationView(TemplateView):
    model_to_recommend: Model = None
    place: str = None
    location: str = None
    kind: str = None
    recommendation_log_model: Model = None
    slice_recommedations: int = None

    def get_recommendation_log_model(self) -> Model:
        if not self.recommendation_log_model:
            model_to_recommend_name = self.model_to_recommend._meta.object_name
            user = "User"
            if self.request.is_visiteur:
                user = "Visiteur"
            object_name = f"{user}{model_to_recommend_name}Recommended"
            return apps.get_model("recsys", object_name, require_ready=True)

        return self.recommendation_log_model
    
    def create_recommendations(
        self,
        recommendations: Union[QuerySet, List],
        recommendation_explained: Dict = None
        ) -> List:
        """
        recommendation_explained may be empty and the explcations of the recommendations could come inside
        the recommendations list
        The recommendation model is created and return a list of all of them that will be used
        """
        recommendation_log_model = self.get_recommendation_log_model()
        user = self.request.visiteur if self.request.is_visiteur else self.request.user
        final_recommendations = []
        for recommendation in recommendations:
            recom = recommendation_log_model.objects.create(
                user=user,
                place=self.place,
                location=self.location,
                kind=self.kind,
                recommendation_explained=recommendation_explained,
                model_recommended=recommendation
            )
            final_recommendations.append(recom)
            
        return final_recommendations
    
    def generate_recommendations(self) -> Union[QuerySet, List]:
        """
        Meant to be overwritten and return the list or queryset of recommendations
        """
        return
    
    def generate_recommendations_explanations(self) -> Union[Dict, List]:
        """
        Meant to be overwritten and return the list or a dict with the recommendations
        explanations
        """
        return
    
    def return_recommendations(self,
        ) -> Union[QuerySet, List]:
        recommendations = self.generate_recommendations()
        recommendations_explanations = self.generate_recommendations_explanations()
        if self.slice_recommedations:
            recommendations = recommendations[:self.slice_recommedations]
        final_recommendations = self.create_recommendations(recommendations, recommendations_explanations)
        return final_recommendations
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "recommendations": self.return_recommendations()
            }
        )
        return context


class BaseCompanyVisitedRecommendationView(BaseRecommendationView):
    model_to_recommend = Company

    def get_specific_company_recommendations(
        self, 
        companies_visited: List
    ) -> QuerySet:
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
        return Company.objects.related_companies_most_visited(
            sectors,
            industries,
            countries,
            exchanges,
        )
    
    def get_random_companies_recommendations(self) -> QuerySet:
        return Company.objects.get_most_visited_companies()
            
    def get_companies_visited(self) -> Union[None, List]:
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
        
    def generate_recommendations(self) -> Union[QuerySet, List]:
        companies_visited = self.get_companies_visited()
        if companies_visited:
            recommendations =  self.get_specific_company_recommendations(companies_visited)
        else:
            recommendations = self.get_random_companies_recommendations()
        return recommendations
    
    def generate_recommendations_explanations(self) -> Union[Dict, List]:
        """
        Meant to be overwritten and return the list or a dict with the recommendations
        explanations
        """
        return {
            "reason": "most_total_visits",
            "sliced": True,
            "slice_size": 5
            }


class CompaniesRecommendedSide(BaseCompanyVisitedRecommendationView):
    template_name = 'company/side_recsys.html'
    place = constants.SIDE
    location = constants.ALL_WEB
    kind = constants.LISTA
    slice_recommedations = 5
