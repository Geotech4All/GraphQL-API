import graphene
from graphene_django.filter import DjangoFilterConnectionField

from assets.graphql.types import FileType, ImageType, TagType
from assets.models import File, Image, Tag
from assets.utils import get_file, get_image


class AssetsQuery(graphene.ObjectType):
    images = DjangoFilterConnectionField(ImageType)
    image = graphene.Field(ImageType, image_id=graphene.ID(required=True))
    files = DjangoFilterConnectionField(FileType)
    file = graphene.Field(FileType, file_id=graphene.ID(required=True))
    tags = DjangoFilterConnectionField(TagType)

    def reslove_images(root, info, **kwargs):
        return Image.objects.all()

    def resolve_image(root, info, **kwargs):
        return get_image(id=str(kwargs.get("image_id")))

    def resolve_files(root, info, **kwargs):
        return File.objects.all()

    def resolve_file(root, info, **kwargs):
        return get_file(id=str(kwargs.get("file_id")))

    def resolve_tags(root, info, **kwargs):
        return Tag.objects.all()
