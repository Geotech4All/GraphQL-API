from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from podcast.models import Address, Event, EventImage, Opportuinity, Organization, Guest, Podcast
from users.graphql.types import UserType

User = get_user_model()

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
    image = graphene.String()
    class Meta:
        model = Guest
        fields = ("id", "name", "description", "organization")
    
    def resolve_image(self, _):
        if isinstance(self, Guest):
            return self.get_image_url
        return None


class PodcastType(DjangoObjectType):
    """
    Podcast graphql object type
    """
    podcast_id = graphene.ID()
    audio = graphene.String()
    guests = graphene.List(GuestType)
    hosts = graphene.List(UserType)
    class Meta:
        model = Podcast
        fields = ("title", "description", "audio", "date_added", "last_updated")
        filter_fields = {
            "id": ["exact"],
            "title": ["icontains", "istartswith", "exact"],
        }
        interfaces = (graphene.relay.Node, )

    def resolve_guests(self, _):
        if isinstance(self, Podcast):
            return getattr(self, "guests").all()

    def resolve_hosts(self, _):
        if isinstance(self, Podcast):
            podcast:Podcast = Podcast.objects.get(pk=self.pk)
            print(podcast.hosts.all())
            return podcast.hosts.all()

    def resolve_audio(self, _):
        if isinstance(self, Podcast):
            return self.get_audio_url()
        return None

    def resolve_podcast_id(self, _):
        if isinstance(self, Podcast):
            return getattr(self, "id")
        return None

class EventType(DjangoObjectType):
    """
    Event graphql object type
    """
    class Meta:
        model = Event
        fields = ("id", "organizer", "title", "description", "date", "venue")


class EventImageType(DjangoObjectType):
    """
    EventImage graphql object type
    """
    image = graphene.String()
    class Meta:
        model = EventImage
        fields = ("id", "description", "event")

    def resolve_image(self, info: graphene.ResolveInfo):
        if isinstance(self, EventImage):
            return self.get_image_url()
        return None


class OpportunityType(DjangoObjectType):
    """
    Oportunity graphql object type
    """
    class Meta:
        model = Opportuinity
        fields = ("id", "title", "description", "start_date", "deadline", "organization")
