from django.shortcuts import render,redirect

from django.db.models import Q

from apps.escritos.models import Term, TermsRelatedToResume
from apps.public_blog.models import PublicBlog
from apps.preguntas_respuestas.models import Question


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

    model_filtered = model.filter(Q(title_icontains=slug) | Q(slug__icontains=slug))
    if model_filtered.exists():
        redirect_to = model_filtered[0].get_absolute_url()
        return redirect(redirect_to)
    else:
        second_model = Term.objects.filter(Q(title_icontains=slug) | Q(slug__icontains=slug))
        if second_model.exists():
            redirect_to = model_filtered[0].get_absolute_url()
            return redirect(redirect_to)
        else:
            old_url = TermsRelatedToResume.objects.filter(Q(term_to_delete__slug__icontains=slug))
            if old_url.exists():
                redirect_to = old_url[0].get_absolute_url()
            else:
                redirect_to = 'general:escritos'
        return redirect(redirect_to)
        
