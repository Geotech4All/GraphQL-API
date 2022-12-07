import graphene
from graphene_django import DjangoObjectType
from podcast.models import Address, EventImage, Organization, Guest, Podcast


class AddressNode(DjangoObjectType):
    """
    Address graphql object type
    """
    class Meta:
        model = Address
        fields = (
            "id",
            "city",
            "state",
            "country",
            "address",
            "zip_code",
            "date_added",
            "last_updated")
                   

class OrganizationType(DjangoObjectType):
    """
    Organization graphql object type
    """
    logo = graphene.String()
    class Meta:
        model = Organization
        fields = ("id", "name", "address", "description", "logo", "email", "phone")

    def resolve_logo(self, info: graphene.ResolveInfo):
        if isinstance(self, Organization):
            return self.get_logo_url()
        return None


class GuestType(DjangoObjectType):
    """
    Guest graphql object type
    """
    class Meta:
        model = Guest
        fields = ("id", "name", "description", "organization")


class PodcastType(DjangoObjectType):
    """
    Podcast graphql object type
    """
    audio = graphene.String()
    class Meta:
        model = Podcast
        fields = ("id", "title", "description", "host", "guest", "audio", "date_added", "last_updated")


    def resolve_audio(self, info: graphene.ResolveInfo):
        if isinstance(self, Podcast):
            return self.get_audio_url()
        return None


class EventImageType(DjangoObjectType):
    """
    EventImage graphql object type
    """
    image = graphene.String()
    class Meta:
        model = EventImage
        fields = ("id", "description")

    def resolve_image(self, info: graphene.ResolveInfo):
        if isinstance(self, EventImage):
            return self.get_image_url()
        return None
