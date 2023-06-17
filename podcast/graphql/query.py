from django.db.models import QuerySet
import graphene
from graphql.error import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from podcast.graphql.types import GuestType, PodcastType
from podcast.models import Guest, Host, Podcast
from users.graphql.types import UserType


class PodcastQuery(graphene.ObjectType):
    all_podcasts = DjangoFilterConnectionField(PodcastType)
    get_podcast_by_id = graphene.Field(PodcastType, podcast_id=graphene.ID(required=True))
    previous_guests = DjangoFilterConnectionField(GuestType)
    most_listened_to_podcasts = DjangoFilterConnectionField(PodcastType)
    get_guest_by_id = graphene.Field(
        GuestType,
        guest_id=graphene.ID(required=True))
    recent_hosts = graphene.List(UserType)

    def resolve_all_podcasts(root, info, **kwargs):
        return Podcast.objects.all().order_by("-date_added")

    def resolve_get_podcast_by_id(root, info, **kwargs):
        id = kwargs.get("podcast_id")
        if not id:
            raise GraphQLError("podcast_id is required")
        try:
            return Podcast.objects.get(pk=id)
        except Podcast.DoesNotExist:
            raise GraphQLError("Podcast with the specified `id` was not found")

    def resolve_previous_guests(root, info, **kwargs):
        return Guest.objects.all()

    def resolve_most_listened_to_podcasts(root, info, **kwargs):
        return Podcast.objects.all().order_by("-listens")

    def resolve_get_guest_by_id(root, info, **kwargs):
        guest_id = kwargs.get("guest_id")
        try:
            return Guest.objects.get(pk=guest_id)
        except Guest.DoesNotExist:
            raise GraphQLError("The sepcified guest was not found")

    def resolve_recent_hosts(root, info, **kwargs):
        users = set()
        hosts: QuerySet[Host] = Host.objects.all().select_related("user").distinct("user__id")
        for host in hosts:
            users.add(host.user)
        return users

