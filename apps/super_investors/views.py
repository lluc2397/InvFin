from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from apps.seo.views import SEOListView, SEODetailView

from .models import Superinvestor


class AllSuperinvestorsView(SEOListView):
    model = Superinvestor
    context_object_name = "superinvestors"
    meta_title = "Las carteras de los mejores inversores del mundo"
    meta_description = "Descubre todas las carteras de los mejores inversores del mundo entero"
    meta_tags = 'empresas, inversiones, analisis de empresas, invertir'


class SuperinvestorView(SEODetailView):
    model = Superinvestor
    context_object_name = "superinvestor"
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    meta_tags = 'empresas, inversiones, analisis de empresas, invertir'