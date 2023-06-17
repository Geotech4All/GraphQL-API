from django.contrib.auth import get_user_model
from django.db import models

from assets.models import File, Image
from common.models import Organization

User = get_user_model()
USER_PLACEHOLDER_IMAGE = "https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_960_720.png"
LOGO_PLACEHOLDER = "https://www.pngkey.com/png/detail/233-2332677_image-500580-placeholder-transparent.png"


class Guest(models.Model):
    """
    This currently refers to a guest on a podcast
    """
    image = models.ImageField(upload_to="images/guests", null=True, blank=True)
    name = models.CharField(max_length=255, help_text="The full name of the guest")
    description = models.TextField(max_length=500, help_text="more information about this guest")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.name}"

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        else:
            return USER_PLACEHOLDER_IMAGE


class Podcast(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, help_text="short summary of this podcast")
    guests = models.ManyToManyField(Guest, related_name="podcasts")
    listens = models.PositiveIntegerField(default=0)
    cover_photo = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    audio = models.ForeignKey(File, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    #TODO: Add podcast scheduled and url
    # scheduled = models.DateTimeField(null=True)
    # url = models.URLField(null=True)

    class Meta:
        ordering = ["date_added", "last_updated"]

    def __str__(self) -> str:
        return f"{self.pk} - {self.title}"

    def get_audio_url(self):
        if self.audio and hasattr(self.audio, 'url'):
            return self.audio.url
        return None

    def get_image_url(self):
        if self.cover_photo and hasattr(self.cover_photo, "url"):
            return self.cover_photo.url
        return None


class Host(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    podcast = models.ForeignKey(Podcast, on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("user", "date_added")
