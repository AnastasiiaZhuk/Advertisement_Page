from django.contrib import admin

from advertisement.models import Advertisement, Heading


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Heading)
# Register your models here.
