from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.contrib.sitemaps.views import sitemap

from rest_framework.documentation import include_docs_urls

from apps.api.views import obtain_auth_key

from apps.seo.sitemaps import (
    TermSitemap,
    QuestionSitemap,
    CompanySitemap,
    PublicBlogSitemap
)

sitemaps = {
    'blogs':PublicBlogSitemap,    
    'preguntas':QuestionSitemap,
    'empresas':CompanySitemap,
    'glosario':TermSitemap
}

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.SECOND_ADMIN_URL, include('admin_honeypot.urls', namespace='admin_honeypot')),
    path("", include("apps.general.urls", namespace="general")),
    path("", include("apps.web.urls", namespace="web")),
    path("", include("apps.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),    
    path("", include("apps.preguntas_respuestas.urls", namespace="preguntas_respuestas")),
    path("", include("apps.escritos.urls", namespace="escritos")),
    path("", include("apps.public_blog.urls", namespace="public_blog")),
    path("screener/", include("apps.screener.urls", namespace="screener")),
    path("", include("apps.super_investors.urls", namespace="super_investors")),    
    path("", include("apps.empresas.urls", namespace="empresas")),
    # path("", include("apps.etfs.urls", namespace="etfs")),
    path("", include("apps.cartera.urls", namespace="cartera")),
    path("", include("apps.seo.urls", namespace="seo")),
    path("", include("apps.roboadvisor.urls", namespace="roboadvisor")),
    path("", include("apps.business.urls", namespace="business")),
    path("", include("apps.recsys.urls", namespace="recsys")),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("apps.api.urls")),
    # DRF auth token
    path("api/obtener-clave/", obtain_auth_key),
]

handler403 = "apps.web.views.handler403"
handler404 = "apps.web.views.handler404"
handler500 = "apps.web.views.handler500"

if settings.DEBUG:
    
    if "drf_spectacular" in settings.INSTALLED_APPS:
        from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
        urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="api-schema"),
            name="api-docs",
        )
    ]
    
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
