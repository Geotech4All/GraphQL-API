import graphene
from graphql.error import GraphQLError
from podcast.graphql.types import AddressNode, EventImageType, GuestType, PodcastType
from podcast.models import Address, EventImage, Guest, Podcast

class PodcastQuery(graphene.ObjectType):
    all_podcasts = graphene.List(PodcastType)
    all_event_images = graphene.List(EventImageType)
    get_guest_by_id = graphene.Field(
        GuestType,
        guest_id=graphene.ID(required=True))
    get_address_by_id = graphene.Field(
        AddressNode,
        address_id=graphene.ID(required=True))


    def resolve_all_podcasts(root, info, **kwargs):
        return Podcast.objects.all()


    def resolve_all_event_images(root, info, **kwargs):
        return EventImage.objects.all()


    def resolve_get_address_by_id(root, info, **kwargs):
        address_id = kwargs.get('address_id')
        try:
            return Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            raise GraphQLError("The specified address was not found")


    def resolve_get_guest_by_id(root, info, **kwargs):
        guest_id = kwargs.get("guest_id")
        try:
            return Guest.objects.get(pk=guest_id)
        except Guest.DoesNotExist:
            raise GraphQLError("The sepcified guest was not found")
