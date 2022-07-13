from datetime import datetime

from apps.seo.models import UserCompanyVisited, VisiteurCompanyVisited
from apps.seo.utils import SeoInformation

from .models import Company


def save_search(request, model_visited):
    """
    When visiteur will be implemented in the request, retreive the visiteur from there
    """
    if request.user.is_authenticated:
        user = request.user
        save_model = UserCompanyVisited
    else:
        user = SeoInformation().find_visiteur(request)
        save_model = VisiteurCompanyVisited
    
    save_model.objects.create(
        user=user,
        model_visited=model_visited,
        date=datetime.now()
    )


def company_searched(search, request):
    empresa_ticker = search.split(' [')[1]
    ticker = empresa_ticker[:-1]
    try:
        empresa_busqueda = Company.objects.get(ticker = ticker)
        redirect_path = empresa_busqueda.get_absolute_url()
        save_search(request, empresa_busqueda)
    except Exception as e:
        redirect_path = request.META.get('HTTP_REFERER')
    
    return redirect_path
