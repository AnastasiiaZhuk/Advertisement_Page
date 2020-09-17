from django.views.generic import DetailView, CreateView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from advertisement.models import Advertisement, SubRubric
from advertisement.middlewares import listing
from advertisement.forms import AdvertisementForm


class AdvertisementDetail(DetailView):
    queryset = Advertisement.objects.all()
    template_name = 'advertisement/advertisement_detail.html'
    context_object_name = 'advertisement'


class AdvertisementAddView(CreateView):
    form_class = AdvertisementForm
    model = Advertisement
    template_name = 'advertisement/add_advs.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AdvertisementAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('advertisement:advertisement_list')


def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    context = listing(request, pk)
    context['rubric'] = rubric
    return render(request, 'advertisement/by_rubric.html', context)


def detail(request, pk):
    adv = get_object_or_404(Advertisement, pk=pk)
    additional_images = adv.additionalimage_set.all()
    context = {'advertisement': adv, 'ais': additional_images}
    return render(request, 'advertisement/detail.html', context)


def by_main_page(request):
    context = listing(request)
    return render(request, 'home.html', context)