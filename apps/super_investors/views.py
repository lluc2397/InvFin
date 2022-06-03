from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from apps.empresas.models import (
    Company, 
    ExchangeOrganisation
)
from apps.etfs.models import Etf
from apps.empresas.company.update import UpdateCompany
from apps.seo.views import SEOListView, SEODetailView

from .models import Superinvestor


class AllSuperinvestorsView(SEOListView):
    model = Superinvestor
    context_object_name = "superinvestors"
    meta_title = "Las carteras de los mejores inversores del mundo"


class SuperinvestorView(SEODetailView):
    model = Superinvestor
    template_name = 'superinvestsssors/details.html'
    context_object_name = "superinvestor"
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    meta_tags = 'empresas, inversiones, analisis de empresas, invertir'