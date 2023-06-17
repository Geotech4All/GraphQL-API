from django.contrib import admin

from assets.models import File, Image, Tag

admin.site.register(Tag)
admin.site.register(File)
admin.site.register(Image)
