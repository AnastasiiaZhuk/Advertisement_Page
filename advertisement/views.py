from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from advertisement.models import (
    Advertisement, SubRubric,
     AdditionalImage, Comment
)
from advertisement.middlewares import listing
from advertisement.forms import (
    AdvertisementForm, AIFormSet,
    GuestCommentForm, UserCommentForm
)


class AdvertisementDetail(DetailView):
    queryset = Advertisement.objects.all()
    template_name = 'advertisement/advertisement_detail.html'
    context_object_name = 'advertisement'


class AdvertisementAddView(LoginRequiredMixin, CreateView):
    template_name = 'advertisement/add_advs.html'
    model = Advertisement
    form_class = AdvertisementForm

    def get_context_data(self, **kwargs):
        context = super(AdvertisementAddView, self).get_context_data(**kwargs)
        context['formset'] = AIFormSet(queryset=AdditionalImage.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        form = AdvertisementForm(request.POST, request.FILES)
        form.instance.author = request.user
        formset = AIFormSet(request.POST, request.FILES)
        if formset.is_valid() and form.is_valid():
            return self.form_valid(formset, form)

    def form_valid(self, formset, form):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        form.instance = self.object
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('advertisement:advertisement_list')


@login_required
def profile_adv_update(request, pk):
    adv = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=adv)
        if form.is_valid():
            adv = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=adv)
            if formset.is_valid():
                formset.save()
                return redirect('advertisement:advertisement_list')
    else:
        form = AdvertisementForm(instance=adv)
        formset = AIFormSet(instance=adv)
    context = {'form': form, 'formset': formset}
    return render(request, 'advertisement/profile_adv_change.html', context)


@login_required
def profile_adv_delete(request, pk):
    adv = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        adv.delete()
        return redirect('advertisement:advertisement_list')
    else:
        context = {'adv': adv}
        return render(request, 'advertisement/profile_adv_delete.html', context)


def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    context = listing(request, pk)
    context['rubric'] = rubric
    return render(request, 'advertisement/by_rubric.html', context)


def detail(request, pk):
    adv = get_object_or_404(Advertisement, pk=pk)
    additional_images = adv.additionalimage_set.all()
    comments = Comment.objects.filter(adv=pk, is_active=True)
    initial = {'adv': adv.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Comment created')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Comment not created')
    context = {
        'advertisement': adv,
        'ais': additional_images,
        'form': form,
        'comments': comments,
    }
    return render(request, 'advertisement/detail.html', context)


def by_main_page(request):
    context = listing(request)
    return render(request, 'home.html', context)