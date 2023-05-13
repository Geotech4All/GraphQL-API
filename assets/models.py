from typing import Any, Dict, Tuple
from django.db import models
from cloudinary import uploader as cu


class ImageFolders(models.TextChoices):
    BLOG = "BLOG"
    PODCAST = "PODCAST"
    PROFILE = "PROFILE"
    OPPORTUNITY = "OPPORTUNITY"

class Image(models.Model):
    public_id = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True)
    folder = models.CharField(max_length=50, choices=ImageFolders.choices, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_added",)

    @classmethod
    def new(cls, image: Any, description: str|None=None, folder: str|None=None):
        updload_data = cu.upload_image(image, folder=f"images/{folder}")

        new_image: Image = Image.objects.create(
                public_id=updload_data.public_id,
                url=updload_data.url,
                description=description,
                folder=folder)
        new_image.save()
        return new_image

    def delete(self, using: Any = ..., keep_parents: bool = ...) -> Tuple[int, Dict[str, int]]:
        cu.destroy(self.public_id)
        return super().delete(using, keep_parents)

    def update(self, image: Any=None, description: str|None=None):
        if image: cu.upload(image, public_id=self.public_id)
        if description: self.description = description
        self.save()
        return self


class FileFolders(models.TextChoices):
    PODCAST = "PODCAST"

class File(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    public_id = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    folder = models.CharField(max_length=50, choices=FileFolders.choices, null=True)


    @classmethod
    def new(cls, file: Any, name: str, description:str|None=None, folder:str|None=None):
        from assets.utils import CloudinaryType
        response:CloudinaryType = CloudinaryType(**cu.upload(file, folder=f"files/{folder}", resource_type="raw"))
        new_file: File = File.objects.create(
                name=name,
                url=response.url,
                description=description,
                public_id=response.public_id,
                folder=folder)
        new_file.save()
        return new_file

    def delete(self, using: Any = ..., keep_parents: bool = ...) -> Tuple[int, Dict[str, int]]:
        cu.destroy(self.public_id)
        return super().delete(using, keep_parents)

    def update(self, file: Any|None=None, name:str|None=None, description:str|None=None):
        if file: cu.upload(file, public_id=self.public_id)
        if name: self.name = name
        if description: self.description = description
        self.save()
        return self


class Tag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=500, null=True)
    category = models.CharField(max_length=255)
