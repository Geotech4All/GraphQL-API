from django.contrib.auth import get_user_model
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.db import models

User = get_user_model()
USER_PLACEHOLDER_IMAGE = "https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_960_720.png"
LOGO_PLACEHOLDER = "https://www.pngkey.com/png/detail/233-2332677_image-500580-placeholder-transparent.png"

class Address(models.Model):
    """
    This will mainly refer to the address of an organization or establishment,
    but can be used as a regular address as well.
    """
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
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
    description = models.CharField(max_length=400, null=True)
    logo = models.ImageField(upload_to="images/organizations", null=True)
    email = models.EmailField(null=True, blank=True, max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def get_logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return LOGO_PLACEHOLDER


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

# TODO: Conver Podcast cover_photo to use Image table

class Podcast(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, help_text="short summary of this podcast")
    guests = models.ManyToManyField(Guest, related_name="podcasts")
    listens = models.PositiveIntegerField(default=0)
    cover_photo = models.ImageField(upload_to="images/podcasts", null=True, blank=True)
    audio = models.FileField(
        storage=RawMediaCloudinaryStorage(),
        upload_to="uploads/podcast",
        null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

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


class Event(models.Model):
    organizer = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=700, help_text="what's this event about")
    date = models.DateField(null=True, blank=True)
    venue = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.title}"


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/events")
    description = models.CharField(max_length=255, help_text="what's in this image", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - Image:{self.description}"

    def get_image_url(self):
        if hasattr(self.image, 'url'):
            return self.image.url
        return None

