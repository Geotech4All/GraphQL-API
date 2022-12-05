from django.contrib.auth import get_user_model
from django.db import models
from django_countries.fields import CountryField

from podcast.validators import FileValidator

User = get_user_model()

class Address(models.Model):
    """
    This will mainly refer to the address of an organization or establishment,
    but can be used as a regular address as well.
    """
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.address}"


class Organization(models.Model):
    """
    This as of the time of writing, mostly refers to the organisers of an event.
    """
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    description = models.CharField(max_length=400)
    logo = models.ImageField(upload_to="images/organizations")
    email = models.EmailField(null=True, blank=True, max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Guest(models.Model):
    """
    This currently refers to a guest on a podcast
    """
    name = models.CharField(max_length=255, help_text="The full name of the guest")
    description = models.TextField(max_length=500, help_text="more information about this guest")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.name}"

validate_file = FileValidator(content_types=('audio/x-mp3', 'audio/mp4', 'audio/mpeg', 'application/ogg', 'audio/x-mp2'))

class Podcast(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, help_text="short summary of this podcast")
    host = models.ForeignKey(User, on_delete=models.PROTECT)
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT)
    audio = models.FileField(validators=[validate_file])
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.title}"


class EventImage(models.Model):
    image = models.ImageField(upload_to="images/events")
    description = models.CharField(max_length=255, help_text="what's in this image", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - Image:{self.description}"


class Event(models.Model):
    organizer = models.ForeignKey(Organization, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=700, help_text="what's this event about")
    date = models.DateField()
    venue = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)
    images = models.ManyToManyField(EventImage)


class Oportunity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="details of this oportunity")
    company = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
