from django.db import models
from assets.models import Image, Tag

class Organization(models.Model):
    """
    Refers to the organization / source of an opportunity
    """
    name = models.CharField(max_length=300)
    description = models.TextField(null=True)
    logo = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)


class Location(models.Model):
    """
    Can be used with Organization, Events etc.
    """
    country = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    zip_code = models.CharField(max_length=20, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
