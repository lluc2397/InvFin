from django.shortcuts import render

from apps.seo.views import SEOListView, SEODetailView

from .models import Superinvestor, SuperinvestorActivity


class AllSuperinvestorsView(SEOListView):
    model = Superinvestor
    paginate_by = 5
    context_object_name = "superinvestors"
    meta_title = "Las carteras de los mejores inversores del mundo"
    meta_description = "Descubre todas las carteras de los mejores inversores del mundo entero"
    meta_tags = 'empresas, inversiones, analisis de empresas, invertir'

    def get_queryset(self):
        return super().get_queryset()


class SuperinvestorView(SEODetailView):
    model = Superinvestor
    context_object_name = "superinvestor"
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    meta_tags = 'empresas, inversiones, analisis de empresas, invertir'

    def get_object(self):
        return self.model.objects.prefetch_related(
            'history',
            'history__period_related'
        ).get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investor = self.object
        is_fav = False
        if self.request.user.is_authenticated:
            if investor.slug in self.request.user.fav_superinvestors.only('slug'):
                is_fav = True
        context['is_fav'] = is_fav
        return context


def return_superinvestor_movements(request, id):
    all_activity = SuperinvestorActivity.objects.prefetch_related(
            'period_related'
        ).filter(superinvestor_related_id=id)
    return render(request, 'super_investors/tables/activity.html', {'all_activity': all_activity})