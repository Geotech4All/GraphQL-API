from django.contrib import admin

from podcast.models import Guest, Organization, Podcast

# Register your models here.

admin.site.register(Guest)
admin.site.register(Organization)
admin.site.register(Podcast)
