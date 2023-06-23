from django.db import models

from assets.models import Tag
from common.models import Location, Organization


class Opportunity(models.Model):
    """
    Can refer to an internship, job-listing, conferences, webinars, scholarship
    """
    title = models.CharField(max_length=225)
    content = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # Updates
    description = models.CharField(null=True, max_length=1000)
    tags = models.ManyToManyField(Tag, related_name="opportunities")
    organization = models.ForeignKey(Organization, blank=True, on_delete=models.SET_NULL, null=True)
    location = models.ManyToManyField(Location, blank=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.date_added.date()}"

    class Meta:
        verbose_name_plural = "opportunities"
        ordering = ("-last_updated", )
