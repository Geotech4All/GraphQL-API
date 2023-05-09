from django.db import models

from assets.models import Image, Tag


class Opportunity(models.Model):

    title = models.CharField(max_length=225)
    description = models.TextField(null=True)
    images = models.ManyToManyField(Image)
    category = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-last_updated", )
