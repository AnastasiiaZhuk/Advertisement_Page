from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from user.models import AdvUser


class CustomUserCreationForm(UserCreationForm):

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        user.is_activated = False

        if commit:
            user.save()
        return user
    
    class Meta:
        model = get_user_model()
        fields = (
            'email', 'username', 'password1',
            'password2', 'send_message'
        )


class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = AdvUser

        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'send_message'
        )
