from django.db import models

from assets.models import Tag


class Opportunity(models.Model):

    title = models.CharField(max_length=225)
    abstract = models.TextField(null=True)
    content = models.TextField(null=True)
    category = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-last_updated", )
