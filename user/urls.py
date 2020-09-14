from django.urls import path

from user.views import SignIn, LogOut,\
    SignUp, user_activate_by_email,\
    ChangeUserInfoView, profile,\
    PasswordChange

app_name = 'accounts'
urlpatterns = [
    path('sign_in/', SignIn.as_view(), name='sign_in'),
    path('log_out/', LogOut.as_view(), name='log_out'),
    path('sign_up/', SignUp.as_view(), name='register'),
    path('user/profile/', profile, name='profile'),
    path('user/activate/<str:sign>/', user_activate_by_email, name='register_activate'),
    path('user/change/', ChangeUserInfoView.as_view(), name='change_info'),
    path('user/password/change/', PasswordChange.as_view(), name='password_change')
]