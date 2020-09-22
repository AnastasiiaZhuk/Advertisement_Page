from captcha.fields import CaptchaField
from django import forms

from advertisement.models import \
    SubRubric, SuperRubric,\
    Advertisement, AdditionalImage,\
    Comment


class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(
        queryset=SuperRubric.objects.all(),
        empty_label=None,
        required=True,
        label='SubRubric',
    )

    class Meta:
        model = SubRubric
        fields = '__all__'


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='', required=False)


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        exclude = ('author',)


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = {'is_active'}
        widgets = {'adv': forms.HiddenInput}


class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(
        label='Input text from the photo',
        error_messages={'invalid': 'Invalid text'}
    )

    class Meta:
        model = Comment
        exclude = {'is_active'}
        widgets = {'adv': forms.HiddenInput}


AIFormSet = forms.inlineformset_factory(Advertisement, AdditionalImage, fields='__all__')

