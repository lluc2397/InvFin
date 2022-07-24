from django.contrib.sitemaps import Sitemap

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.super_investors.models import Superinvestor


class SuperinvestorSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Superinvestor.objects.all()

    def location(self,obj):
        return obj.get_absolute_url()


class PublicBlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return PublicBlog.objects.filter(status = 1)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self,obj):
        return obj.custom_url


class TermSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Term.objects.filter(status = 1)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self,obj):
        return obj.get_absolute_url()


class CompanySitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Company.objects.filter(
            no_incs = False,
            no_bs = False,
            no_cfs = False,
        )

    def location(self,obj):
        return obj.get_absolute_url()


class QuestionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Question.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self,obj):
        return obj.get_absolute_url()