from django.contrib.auth import get_user_model
import graphene
from graphql import GraphQLError
from podcast.models import (
    Address,
    Event,
    EventImage,
    Organization,
    Guest,
    Podcast,
    Opportuinity)
from users.models import CustomUser, Staff

User = get_user_model()

def validate_staff(info: graphene.ResolveInfo):
    try:
        Staff.objects.get(user=info.context.user)
    except Staff.DoesNotExist:
        raise GraphQLError("You are not authorised to perform this action")


def get_user(user_id: str | int) -> CustomUser:
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise GraphQLError("User with the specified `id` was not found")


def get_organization(organization_id: str | int) -> Organization:
    try:
        return Organization.objects.get(pk=organization_id)
    except Organization.DoesNotExist:
        raise GraphQLError("Organization with the specified `id` was not found")


def get_address(address_id: str | int) -> Address:
    try:
        return Address.objects.get(pk=address_id)
    except Address.DoesNotExist:
        raise GraphQLError("Address with the specified `id` was not found")


def get_guest(guest_id: str | int) -> Guest:
    try:
        return Guest.objects.get(pk=guest_id)
    except Guest.DoesNotExist:
        raise GraphQLError("Guest with the specified `id` was not found")


def get_podcast(podcast_id: str | int) -> Podcast:
    try:
        return Podcast.objects.get(pk=podcast_id)
    except Podcast.DoesNotExist:
        raise GraphQLError("Podcast with the specified `id` was not found")


def get_event_image(event_image_id: str | int) -> EventImage:
    try:
        return EventImage.objects.get(pk=event_image_id)
    except EventImage.DoesNotExist:
        raise GraphQLError("EventImage with the specified `id` was not found")


def get_event(event_id: str | int) -> Event:
    try:
        return Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise GraphQLError("Event with the specified `id` was not found")


def get_opportunity(opportunity_id: str | int) -> Opportuinity:
    try:
        return Opportuinity.objects.get(pk=opportunity_id)
    except Opportuinity.DoesNotExist:
        raise GraphQLError("Opportuinity with the specified `id` was not found")


def perform_address_update(info:graphene.ResolveInfo, **kwargs) -> Address:
    """
    Performs an update operation on address object.
    """
    address_id = kwargs.get('address_id', None)
    if not address_id:
        raise GraphQLError("address_id is required")
    validate_staff(info)
    address: Address = get_address(address_id)
    address.city = kwargs.get('city', address.city)
    address.state = kwargs.get('state', address.state)
    address.country = kwargs.get('country', address.country)
    address.address = kwargs.get('address', address.address)
    address.zip_code = kwargs.get('zip_code', address.zip_code)
    address.save()
    return address

def perform_address_create(info:graphene.ResolveInfo, **kwargs) -> Address:
    """
    Performs create operation on address object.
    """
    validate_staff(info)
    address: Address = Address.objects.create(
        city=kwargs.get('city'),
        state=kwargs.get('state'),
        country=kwargs.get('country'),
        address=kwargs.get('address'),
        zip_code=kwargs.get('zip_code')
        )
    return address


def perform_organization_update(info:graphene.ResolveInfo, **kwargs) -> Organization:
    """
    Performs update operation on organization object.
    """
    organization_id = kwargs.get('organization_id', None)
    address_id = str(kwargs.get('address_id'))
    if not organization_id:
        raise GraphQLError("organization_id is required")
    validate_staff(info)
    organization: Organization = get_organization(organization_id)
    organization.name = kwargs.get('name')
    organization.address = get_address(address_id) if address_id else organization.address
    organization.description = kwargs.get('description', organization.description)
    organization.logo = kwargs.get('logo', organization.logo)
    organization.email = kwargs.get('email', organization.email)    
    organization.phone = kwargs.get('phone', organization.phone)    
    organization.save()
    return organization


def perform_organization_create(info:graphene.ResolveInfo, **kwargs) -> Organization:
    """
    Performs create operation on organization object.
    """
    address_id = str(kwargs.get('address_id'))
    validate_staff(info)
    organization: Organization = Organization.objects.create(
        name = kwargs.get('name'),
        address = get_address(address_id) if address_id else None,
        description = kwargs.get('description'),
        logo = kwargs.get('logo'),
        email = kwargs.get('email'),
        phone = kwargs.get('phone')
    )
    return organization


def perform_guest_update(info:graphene.ResolveInfo, **kwargs) -> Guest:
    """
    Performs update operation on guest object.
    """
    validate_staff(info)

    guest_id = kwargs.get("guest_id")
    organization_id = kwargs.get("organization_id")

    if not guest_id:
        raise GraphQLError("guest_id is required")

    guest = get_guest(guest_id)
    guest.name = kwargs.get("name", guest.name)
    guest.description = kwargs.get("description", guest.description)
    guest.organization = get_organization(organization_id) if organization_id else guest.organization
    guest.save()
    return guest


def perform_guest_create(info:graphene.ResolveInfo, **kwargs) -> Guest:
    """
    Performs create operation on guest object.
    """

    validate_staff(info)
    organization_id = kwargs.get("organization_id")

    guest = Guest.objects.create(
        name=kwargs.get("name"),
        description=kwargs.get("description"),
        organization=get_organization(organization_id) if organization_id else None
        )
    return guest


def perform_podcast_update(info: graphene.ResolveInfo, **kwargs) -> Podcast:
    """
    Performs update operation on Podcast
    """
    validate_staff(info)
    podcast_id = kwargs.get("podcast_id")
    host_id = kwargs.get("host_id")
    guest_id = kwargs.get("guest_id")
    if not podcast_id:
        raise GraphQLError("podcast_id is required")
    if not host_id:
        raise GraphQLError("host_id is required")
    podcast = get_podcast(podcast_id)
    podcast.host = get_user(host_id)
    podcast.title = kwargs.get("title", podcast.title)
    podcast.description = kwargs.get("description", podcast.description)
    podcast.guest = get_guest(guest_id) if guest_id else podcast.guest
    podcast.audio = kwargs.get("audio", podcast.audio)
    podcast.save()
    return podcast


def perform_podcast_create(info: graphene.ResolveInfo, **kwargs) -> Podcast:
    """
    Performs create operation on Podcast
    """
    validate_staff(info)
    host_id = kwargs.get("host_id")
    guest_id = kwargs.get("guest_id")
    if not host_id:
        raise GraphQLError("host_id is required")
    podcast = Podcast.objects.create(
        host=get_user(host_id),
        title=kwargs.get("title"),
        description=kwargs.get("description"),
        audio=kwargs.get("audio"),
        guest=get_guest(guest_id) if guest_id else None
        )
    return podcast


def perform_event_update(info: graphene.ResolveInfo, **kwargs) -> Event:
    """
    Performs update operation on Event.
    """
    validate_staff(info)
    event_id = kwargs.get("event_id")
    organizer_id = kwargs.get("organizer_id")
    address_id = kwargs.get("address_id")
    if not event_id:
        raise GraphQLError("event_id is required")
    event = get_event(event_id)
    event.title = kwargs.get("title", event.title)
    event.description = kwargs.get("description", event.description)
    event.date = kwargs.get("date", event.date)
    event.organizer = get_organization(organizer_id) if organizer_id else event.organizer
    event.venue = get_address(address_id) if address_id else event.venue
    event.save()
    return event


def perform_event_create(info: graphene.ResolveInfo, **kwargs) -> Event:
    """
    Performs create operation on Event.
    """
    validate_staff(info)
    organizer_id = kwargs.get("organizer_id")
    address_id = kwargs.get("address_id")
    event = Event.objects.create(
        title=kwargs.get("title"),
        description=kwargs.get("description"),
        date=kwargs.get("date"),
        organizer=get_organization(organizer_id) if organizer_id else None,
        venue=get_address(address_id) if address_id else None
        )
    return event


def perform_event_image_update(info: graphene.ResolveInfo, **kwargs) -> EventImage:
    """
    Performs update operation on EventImage.
    """
    validate_staff(info)
    event_id = kwargs.get("event_id")
    event_image_id = kwargs.get("event_image_id")
    if not event_image_id:
        raise GraphQLError("event_image_id is required")
    if not event_id:
        raise GraphQLError("event_id is required")
    event_image = get_event_image(event_image_id)
    event_image.image = kwargs.get("image", event_image.image)
    event_image.description = kwargs.get("description", event_image.description)
    event_image.event = get_event(event_id)
    event_image.save()
    return event_image


def perform_event_image_create(info: graphene.ResolveInfo, **kwargs) -> EventImage:
    """
    Performs create operation on EventImage.
    """
    validate_staff(info)
    event_id = kwargs.get("event_id")
    if not event_id:
        raise GraphQLError("event_id is required")
    event_image = EventImage.objects.create(
        image=kwargs.get("image"),
        event=get_event(event_id),
        description=kwargs.get("description"))
    return event_image


def perform_opportunity_update(info: graphene.ResolveInfo, **kwargs) -> Opportuinity:
    """
    Performs update operation on an Opportuinity.
    """
    validate_staff(info)
    opportunity_id = kwargs.get("opportunity_id")
    organization_id = kwargs.get("organization_id")
    if not opportunity_id:
        raise GraphQLError("oportunity_id is required")
    opportunity = get_opportunity(opportunity_id)
    opportunity.title = kwargs.get("title", opportunity.title)
    opportunity.description = kwargs.get("description", opportunity.description)
    opportunity.start_date = kwargs.get("start_date", opportunity.start_date)
    opportunity.deadline = kwargs.get("deadline")
    opportunity.organization = get_organization(organization_id) if organization_id else opportunity.organization
    opportunity.save()
    return opportunity


def perform_opportunity_create(info: graphene.ResolveInfo, **kwargs) -> Opportuinity:
    """
    Performs create operation on an Opportuinity.
    """
    validate_staff(info)
    organization_id = kwargs.get("organization_id")
    opportunity = Opportuinity.objects.create(
        title=kwargs.get("title"),
        description=kwargs.get("description"),
        start_date=kwargs.get("start_date"),
        deadline=kwargs.get("deadline"),
        organization=get_organization(organization_id) if organization_id else None
        )
    return opportunity
