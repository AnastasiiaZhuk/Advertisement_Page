from django.contrib import admin

from user.models import AdvUser


class AdvUserListing(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_activated', 'send_message')


admin.site.register(AdvUser, AdvUserListing)
# Register your models here.
