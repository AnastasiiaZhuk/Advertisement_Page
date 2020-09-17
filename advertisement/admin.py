from django.contrib import admin

from advertisement.models import \
    Advertisement, SuperRubric,\
    SubRubric, AdditionalImage
from advertisement.forms import SubRubricForm


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


class SubRubricInline(admin.TabularInline):
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric', )
    inlines = (SubRubricInline,)


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'author')
    fields = (
        ('rubric', 'author'), 'title',
        'price', 'content',
        'contacts', 'image',
    )
    inlines = (AdditionalImageInline, )


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
# Register your models here.
