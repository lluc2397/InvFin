from django.shortcuts import redirect
from django.views.generic import RedirectView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect

from apps.escritos.models import Term, TermsRelatedToResume
from apps.public_blog.models import PublicBlog
from apps.preguntas_respuestas.models import Question

from .models import Promotion


def redirect_old_urls(request, ques_slug=False, term_slug=False, publs_slug=False):
    if ques_slug == False and term_slug == False:
        model = PublicBlog.objects
        slug = publs_slug

    elif term_slug == False and publs_slug == False:
        model = Question.objects
        slug = ques_slug
        
    elif publs_slug == False and ques_slug == False:
        model = Term.objects
        slug = term_slug

    model_filtered = model.filter(Q(title__icontains=slug) | Q(slug__icontains=slug))
    if model_filtered.exists():
        redirect_to = model_filtered[0].get_absolute_url()
    else:
        second_model = Term.objects.filter(Q(title__icontains=slug) | Q(slug__icontains=slug))
        if second_model.exists():
            redirect_to = second_model[0].get_absolute_url()
        else:
            old_url = TermsRelatedToResume.objects.filter(Q(term_to_delete__slug__icontains=slug))
            if old_url.exists():
                redirect_to = old_url[0].get_absolute_url()
            else:
                redirect_to = 'general:escritos'
    return redirect(redirect_to)
        

class PromotionRedirectView(RedirectView):

    permanent = False

    def save_promotion_data(self, slug):
        model = Promotion.objects.get(slug = slug)
        return model.full_url

    def get(self, request, *args, **kwargs):
        slug = request.GET.kwargs['slug']
        url = self.save_promotion_data(slug)
        return HttpResponseRedirect(url)


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /private/",
        "Disallow: /junk/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


class SEOViewMixin:
    meta_description = None
    meta_tags = 'finanzas, blog financiero, blog el financiera, invertir'
    meta_title = None
    meta_url = None
    meta_image = 'https://inversionesyfinanzas.xyz/static/general/assets/img/favicon/favicon.ico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_desc"] = self.meta_description
        context["meta_tags"] = self.meta_tags
        context["meta_title"] = self.meta_title
        context["meta_url"] = self.meta_url
        context["meta_img"] = self.meta_image
        return context