from django.contrib import admin

from podcast.models import Event, Address, EventImage, Guest, Organization, Podcast

# Register your models here.

admin.site.register(Event)
admin.site.register(Address)
admin.site.register(EventImage)
admin.site.register(Guest)
admin.site.register(Organization)
admin.site.register(Podcast)
