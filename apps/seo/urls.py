from django.urls import path

from .views import (
    redirect_old_urls,
    PromotionRedirectView
)

app_name = "seo"
urlpatterns = [
    path('question/<ques_slug>/', redirect_old_urls, name="question_redirect"),
    path('definicion/<term_slug>/', redirect_old_urls, name="terms_redirect"),
    path('publicaciones/<publs_slug>/', redirect_old_urls, name="publs_redirect"),

    path('aprovecha-la-promocion/<promo_id>/', PromotionRedirectView.as_view(), name="promotion_redirect"),
    
]