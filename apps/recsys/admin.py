from django.contrib import admin
from .models import (
    VisiteurCompanyRecommended,
    VisiteurProductComplementaryRecommended,
    VisiteurPromotionRecommended,
    VisiteurPublicBlogRecommended,
    VisiteurQuestionRecommended,
    VisiteurTermRecommended,
    UserCompanyRecommended,
    UserProductComplementaryRecommended,
    UserPromotionRecommended,
    UserPublicBlogRecommended,
    UserQuestionRecommended,
    UserTermRecommended
)


class BaseModelRecommendededAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'model_recommended',
        "clicked",
        "recommendation_personalized",
        "recommendation_explained",
        "place",
        "location",
        "kind",
        'date',
    ]


@admin.register(VisiteurCompanyRecommended)
class VisiteurCompanyRecommendedAdmin(BaseModelRecommendededAdmin):
    pass


@admin.register(VisiteurProductComplementaryRecommended)
class VisiteurProductComplementaryRecommendedAdmin(BaseModelRecommendededAdmin):
    pass


@admin.register(VisiteurPromotionRecommended)
class VisiteurPromotionRecommendedAdmin(BaseModelRecommendededAdmin):
    pass


@admin.register(VisiteurPublicBlogRecommended)
class VisiteurPublicBlogRecommendedAdmin(BaseModelRecommendededAdmin):
    pass


@admin.register(VisiteurQuestionRecommended)
class VisiteurQuestionRecommendedAdmin(BaseModelRecommendededAdmin):
    pass


@admin.register(VisiteurTermRecommended)
class VisiteurTermRecommendedAdmin(BaseModelRecommendededAdmin):
    pass


@admin.register(UserCompanyRecommended)
class UserCompanyRecommendedAdmin(BaseModelRecommendededAdmin):
    pass


@admin.register(UserProductComplementaryRecommended)
class UserProductComplementaryRecommendedAdmin(BaseModelRecommendededAdmin):
    pass


@admin.register(UserPromotionRecommended)
class UserPromotionRecommendedAdmin(BaseModelRecommendededAdmin):
    pass


@admin.register(UserPublicBlogRecommended)
class UserPublicBlogRecommendedAdmin(BaseModelRecommendededAdmin):
    pass


@admin.register(UserQuestionRecommended)
class UserQuestionRecommendedAdmin(BaseModelRecommendededAdmin):
    pass


@admin.register(UserTermRecommended)
class UserTermRecommendedAdmin(BaseModelRecommendededAdmin):
    pass
