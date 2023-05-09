from typing import Any, Dict, Optional, Tuple
from django.db import models
import cloudinary
import cloudinary.uploader
import cloudinary.api
from graphql import GraphQLError


class Folders(models.TextChoices):
    PROFILE = "PROFILE",
    OPPORTUNITY = "OPPORTUNITY"
    BLOG = "BLOG"

class Image(models.Model):
    public_id = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True)
    folder = models.CharField(max_length=50, choices=Folders.choices, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_added",)

    @classmethod
    def new(cls, image: Any, description: Optional[str] = None, folder: str|None=None):
        updload_data = cloudinary.uploader.upload_image(image, folder=folder)

        new_image: Image = Image.objects.create(
                public_id=updload_data.public_id,
                url=updload_data.url,
                description=description,
                folder=folder)
        new_image.save()
        return new_image

    def delete(self, using: Any = ..., keep_parents: bool = ...) -> Tuple[int, Dict[str, int]]:
        print(self.public_id)
        cloudinary.uploader.destroy(self.public_id)
        return super().delete(using, keep_parents)

    @classmethod
    def update(cls, image_id: str, image: Any=None, description: str|None=None):
        try:
            img: Image = Image.objects.get(id=image_id)
            if image: cloudinary.uploader.upload(image, public_id=img.public_id)
            if description: img.description = description
            img.save()
            return img
        except Image.DoesNotExist:
            raise GraphQLError("Specified image was not found")


class Tag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=500, null=True)
    category = models.CharField(max_length=255)
