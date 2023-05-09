import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from assets.graphql.types import ImageType, TagType
from assets.models import Image, Tag


class AssetsQuery(graphene.ObjectType):
    images = DjangoFilterConnectionField(ImageType)
    image = graphene.Field(ImageType, image_id=graphene.ID(required=True))
    tags = DjangoFilterConnectionField(TagType)

    def reslove_images(root, info, **kwargs):
        return Image.objects.all()

    def resolve_image(root, info, **kwargs):
        try:
            return Image.objects.get(id=kwargs.get("image_id"))
        except Image.DoesNotExist:
            raise GraphQLError("Specified image was not found")

    def resolve_tags(root, info, **kwargs):
        return Tag.objects.all()
