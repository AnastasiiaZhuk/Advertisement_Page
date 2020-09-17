from django.urls import path

from advertisement.views import \
    AdvertisementDetail, AdvertisementAddView,\
    by_rubric, detail, by_main_page

app_name = 'advertisement'

urlpatterns = [
    path('', by_main_page, name='advertisement_list'),
    path('<int:pk>/', AdvertisementDetail.as_view(), name='advertisement_detail'),
    path('rubric/<int:pk>/', by_rubric, name='rubric'),
    path('rubric/info/<int:pk>/', detail, name='detail'),
    path('profile/add/', AdvertisementAddView.as_view(), name='add_adv')
]