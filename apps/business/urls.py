from django.urls import path

from .views import (
    ProductsListView,
    ProductDetailView
)

app_name = "business"
urlpatterns = [
    path('las-mejores-herramientas-para-invertir', ProductsListView.as_view(), name='all_products'),
    path('la-mejor-herramienta-para-invertir-es/<slug>', ProductDetailView.as_view(), name='product'),
]