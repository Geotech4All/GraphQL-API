import graphene
from graphene_django import DjangoObjectType

from assets.models import File, Image, Tag


class ImageType(DjangoObjectType):
    image_id = graphene.ID()
    class Meta:
        model = Image
        fields = ("public_id", "url", "description")
        filter_fields = {"description": ["icontains", "exact", "istartswith"]}
        interfaces = (graphene.relay.Node, )

    def resolve_image_id(self, _):
        if isinstance(self, Image):
            return self.pk
        return None


class FileType(DjangoObjectType):
    file_id = graphene.ID()
    class Meta:
        model = File
        fields = ("name", "description", "url", "public_id")
        filter_fields = {
                "name": ["icontains", "exact", "istartswith"],
                "description": ["icontains", "istartswith"]
            }
        interfaces = (graphene.relay.Node, )

    def resolve_file_id(self, _):
        if isinstance(self, File):
            return self.pk
        return None


class TagType(DjangoObjectType):
    tag_id = graphene.ID()
    class Meta:
        model = Tag
        fields = ("title", "description", "category")
        filter_fields = {"category": ["iexact", "exact"]}
        interfaces = (graphene.relay.Node, )

    def resolve_tag_id(self, _):
        if isinstance(self, Tag):
            return self.pk
        return None
