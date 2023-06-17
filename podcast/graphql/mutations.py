import graphene
from graphene_django.types import ErrorType
from graphql_auth.decorators import login_required
from podcast.graphql.utils.guest_mutations import perform_guest_create, perform_guest_update
from podcast.graphql.utils.podcast_mutations import (
        perform_podcast_create, perform_podcast_update, perform_podcast_listens_increase)
from .types import ( GuestType, PodcastType)


class GuestCreateUpdateMutation(graphene.Mutation):
    """
    Performs create and update actions on a `Guest` object.
    To perform an update all you need to do is pass in the guest `id`.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    guest = graphene.Field(GuestType)

    class Arguments:
        guest_id = graphene.ID(
            description="Pass this if you want to perform an update on a guest")
        name = graphene.String(required=True)
        description = graphene.String()
        organization_id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        guest_id = kwargs.get('guest_id')
        if guest_id:
            guest = perform_guest_update(info, **kwargs)
            return GuestCreateUpdateMutation(success=True, guest=guest)
        guest = perform_guest_create(info, **kwargs)
        return GuestCreateUpdateMutation(success=True, guest=guest)


class PodcastCreateUpdateMutation(graphene.Mutation):
    """
    Performs create and update activity on `Podcast` object.
    To perform an update, all you need to do is pass the podcast `id`.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    podcast = graphene.Field(PodcastType)

    class Arguments:
        podcast_id = graphene.ID(
            description="The `id` of the podcast you want to update")
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        host_ids = graphene.List(graphene.ID, required=True,
            description="A list of `id`s for the host `User` object")
        guest_ids = graphene.List(graphene.ID,
            description="This might not be required since not all podcasts have guests")
        audio_id = graphene.ID()
        cover_photo_id = graphene.ID()


    @classmethod
    @login_required
    def mutate(cls, _, info: graphene.ResolveInfo, **kwargs):
        podcast_id = kwargs.get("podcast_id")
        if podcast_id:
            podcast = perform_podcast_update(info, **kwargs)
            return PodcastCreateUpdateMutation(success=True, podcast=podcast)
        podcast = perform_podcast_create(info, **kwargs)
        return PodcastCreateUpdateMutation(success=True, podcast=podcast)


class IncreasePodcastListens(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    podcast = graphene.Field(PodcastType)

    class Arguments:
        podcast_id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        podcast = perform_podcast_listens_increase(**kwargs)
        return IncreasePodcastListens(success=True, podcast=podcast)


class PodcastMutations(graphene.ObjectType):
    increase_podcast_listens = IncreasePodcastListens.Field()
    create_update_guest = GuestCreateUpdateMutation.Field()
    create_update_podcast = PodcastCreateUpdateMutation.Field()
