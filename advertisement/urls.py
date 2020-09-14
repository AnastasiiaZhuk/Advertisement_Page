from django.urls import path

from advertisement.views import AdvertisementList, AdvertisementDetail

app_name = 'advertisement'

urlpatterns = [
    path('', AdvertisementList.as_view(), name='advertisement_list'),
    path('<int:pk>/', AdvertisementDetail.as_view(), name='advertisement_detail'),
]