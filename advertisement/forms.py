from django import forms

from advertisement.models import \
    SubRubric, SuperRubric,\
    Advertisement, AdditionalImage


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


AIFormSet = forms.inlineformset_factory(Advertisement, AdditionalImage, fields='__all__')