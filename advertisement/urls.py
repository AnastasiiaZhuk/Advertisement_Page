from django.urls import path

from advertisement.views import \
    AdvertisementDetail, AdvertisementAddView,\
    profile_adv_update, profile_adv_delete,\
    by_rubric, detail, by_main_page

app_name = 'advertisement'

urlpatterns = [
    path('', by_main_page, name='advertisement_list'),
    path('<int:pk>/', AdvertisementDetail.as_view(), name='advertisement_detail'),
    path('rubric/<int:pk>/', by_rubric, name='rubric'),
    path('rubric/info/<int:pk>/', detail, name='detail'),
    path('profile/add/', AdvertisementAddView.as_view(), name='add_adv'),
    path('profile/update/<int:pk>/', profile_adv_update, name='update'),
    path('profile/delete/<int:pk>/', profile_adv_delete, name='delete' )
]