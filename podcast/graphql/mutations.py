import graphene
from graphene_django.types import ErrorType
from graphene_file_upload.scalars import Upload
from graphql_auth.decorators import login_required
from podcast.graphql.utils.address_mutations import perform_address_create, perform_address_update
from podcast.graphql.utils.org_mutations import perform_organization_create, perform_organization_update
from podcast.graphql.utils.guest_mutations import perform_guest_create, perform_guest_update
from podcast.graphql.utils.podcast_mutations import (
        perform_podcast_create, perform_podcast_update, perform_podcast_listens_increase)
from podcast.graphql.utils.event_mutations import perform_event_create, perform_event_update
from podcast.graphql.utils.event_image_mutations import perform_event_image_create, perform_event_image_update
from .types import (
    EventImageType,
    EventType,
    OrganizationType,
    AddressNode,
    GuestType,
    PodcastType)


class AddressCreateUpdateMutation(graphene.Mutation):
    """
    Performs create and update activity on an `Address`.
    To perform an update all you need to do is pass in the address `id`.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    address = graphene.Field(AddressNode)

    class Arguments:
        address_id = graphene.ID(description="The `id` of the address to be updated")
        city = graphene.String(required=True)
        state = graphene.String(required=True)
        country = graphene.String(required=True)
        address = graphene.String(required=True)
        zip_code = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        address_id = kwargs.get('address_id')
        if address_id:
            address = perform_address_update(info=info, **kwargs)
            return AddressCreateUpdateMutation(success=True, address=address)
        address = perform_address_create(info, **kwargs)
        return AddressCreateUpdateMutation(success=True, address=address)


class OrganizationCreateUpdateMutation(graphene.Mutation):
    """
    Performs create and update activiies on an `Organization`.
    To perform an update all you need to do is pass the organization `id`.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    organization = graphene.Field(OrganizationType)

    class Arguments:
        organization_id = graphene.ID(description="The `id` of the organization to be updated")
        name = graphene.String(required=True)
        address_id = graphene.ID()
        description = graphene.String()
        logo = Upload()
        email = graphene.String()
        phone = graphene.String()


    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        organization_id = kwargs.get('organization_id')
        if organization_id:
            organization = perform_organization_update(info, **kwargs)
            return OrganizationCreateUpdateMutation(success=True, organization=organization)
        organization = perform_organization_create(info, **kwargs)
        return OrganizationCreateUpdateMutation(success=True, organization=organization)


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


class EventCreateUpdateMutation(graphene.Mutation):
    """
    Performs create and update actions for an event.
    To perform an update all you need to do is pass in the event `id`.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    event = graphene.Field(EventType)

    class Arguments:
        event_id = graphene.ID(
            description="The `id` of the Event to be updated")
        organizer_id = graphene.ID(
            description="If this event is being handled by an organization, pass its `id`")
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        date = graphene.Date()
        address_id = graphene.ID(
            description="If this event has an address of type Address pass its `id`")

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        event_id = kwargs.get("event_id")
        if event_id:
            event = perform_event_update(info, **kwargs)
            return EventCreateUpdateMutation(success=True, event=event)
        event = perform_event_create(info, **kwargs)
        return EventCreateUpdateMutation(success=True, event=event)


class EventImageCreateUpdateMutation(graphene.Mutation):
    """
    Performs create and update actions for an event image.
    To perform an update all you need to do is pass in the event image `id`.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    event_image = graphene.Field(EventImageType)

    class Arguments:
        event_id = graphene.ID(
            required=True,
            description="The `id` of the Event to which this image belongs")
        event_image_id = graphene.ID(
            description="The `id` of the event image to be updated")
        image = Upload()
        description = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        event_image_id = kwargs.get("event_image_id")
        if event_image_id:
            event_image = perform_event_image_update(info, **kwargs)
            return EventImageCreateUpdateMutation(success=True, event_image=event_image)
        event_image = perform_event_image_create(info, **kwargs)
        return EventImageCreateUpdateMutation(success=True, event_image=event_image)


class PodcastMutations(graphene.ObjectType):
    increase_podcast_listens = IncreasePodcastListens.Field()
    create_update_address = AddressCreateUpdateMutation.Field()
    create_update_organization = OrganizationCreateUpdateMutation.Field()
    create_update_guest = GuestCreateUpdateMutation.Field()
    create_update_podcast = PodcastCreateUpdateMutation.Field()
    create_update_event = EventCreateUpdateMutation.Field()
    create_update_event_image = EventImageCreateUpdateMutation.Field()
