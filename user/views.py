from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView

from user.forms import CustomUserCreationForm, CustomUserChangeForm
from user.models import AdvUser
from user.utilities import signer
from advertisement.models import Advertisement


class SignIn(LoginView):
    template_name = 'auth/login.html'


class LogOut(LogoutView):
    template_name = 'auth/logout.html'


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:sign_in')
    template_name = 'auth/register.html'


class ChangeUserInfoView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AdvUser
    template_name = 'auth/update_user.html'
    success_message = 'Information updated!'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('advertisement:advertisement_list')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class PasswordChange(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'auth/password_change.html'
    success_message = 'Password successfully changed'
    success_url = reverse_lazy('accounts:profile')


def user_activate_by_email(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'auth/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'auth/user_is_activated.html'
    else:
        template = 'auth/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


@login_required
def profile(request):
    advs = Advertisement.objects.filter(author=request.user.pk)
    context = {'advertisements': advs}
    return render(request, 'auth/profile.html', context)