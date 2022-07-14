from django.shortcuts import render

from apps.seo.views import SEODetailView, SEOListView

from .models import Superinvestor, SuperinvestorActivity, FavoritesSuperinvestorsList


class AllSuperinvestorsView(SEOListView):
    model = Superinvestor
    paginate_by = 5
    context_object_name = "superinvestors"
    meta_title = "Las carteras de los mejores inversores del mundo"
    meta_description = "Descubre todas las carteras de los mejores inversores del mundo entero"
    meta_tags = 'empresas, inversiones, analisis de empresas, invertir'
    template_name = "superinvestor_list.html"

    def get_queryset(self):
        return super().get_queryset().order_by('name')


class SuperinvestorView(SEODetailView):
    model = Superinvestor
    context_object_name = "superinvestor"
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    meta_tags = 'empresas, inversiones, analisis de empresas, invertir'
    template_name = "superinvestor_detail.html"

    def get_object(self):
        return self.model.objects.prefetch_related(
            'history',
            'history__period_related'
        ).get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investor = self.object
        is_fav = False
        user = self.request.user
        if user.is_authenticated:
            try:
                fav_investors_list = user.fav_superinvestors
            except:
                fav_investors_list, created = FavoritesSuperinvestorsList.objects.get_or_create(user=user)
                fav_investors_list = fav_investors_list.superinvestor
            if investor.slug in fav_investors_list.all().only('slug'):
                is_fav = True
        context['is_fav'] = is_fav
        return context


def return_superinvestor_movements(request, id):
    all_activity = SuperinvestorActivity.objects.prefetch_related(
            'period_related'
        ).filter(superinvestor_related_id=id)
    return render(request, 'tables/activity.html', {'all_activity': all_activity})