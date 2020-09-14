from django.views.generic import ListView, DetailView

from advertisement.models import Advertisement, Heading


class AdvertisementList(ListView):
    template_name = 'home.html'

    queryset = Advertisement.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdvertisementList, self).get_context_data(**kwargs)
        context['headings'] = Heading.objects.all()
        context['advertisements'] = self.queryset
        return context


class AdvertisementDetail(DetailView):
    queryset = Advertisement.objects.all()
    template_name = 'advertisement/advertisement_detail.html'
    context_object_name = 'advertisement'


