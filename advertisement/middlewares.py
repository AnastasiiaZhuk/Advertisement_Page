from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from advertisement.forms import SearchForm
from advertisement.models import SubRubric, Advertisement


def board_context_processor(request):
    context = {
        'keyword': '',
        'all': '',
    }

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']

    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context['all']:
                context['all'] += '&page' + page
            else:
                context['all'] = '?page' + page

    return context


def listing(request, pk=None):
    advs = Advertisement.objects.all()

    if pk:
        advs = Advertisement.objects.filter(is_active=True, rubric=pk)

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        advs = advs.filter(q)
    else:
        keyword = ''

    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(advs, 5)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    context = {
        'page': page, 'advertisements': page.object_list,
        'form': form, 'rubrics': SubRubric.objects.all()
    }
    return context