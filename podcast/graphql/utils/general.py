from django.contrib.auth import get_user_model
import graphene
from graphql import GraphQLError
from podcast.models import (
    Address,
    Event,
    EventImage,
    Host,
    Organization,
    Guest,
    Podcast)
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
        raise GraphQLError(f"User with `id` {user_id} was not found")


def get_organization(organization_id: str | int) -> Organization:
    try:
        return Organization.objects.get(pk=organization_id)
    except Organization.DoesNotExist:
        raise GraphQLError(f"Organization with `id` {organization_id} was not found")


def get_address(address_id: str | int) -> Address:
    try:
        return Address.objects.get(pk=address_id)
    except Address.DoesNotExist:
        raise GraphQLError(f"Address with `id` {address_id} was not found")


def get_guest(guest_id: str | int) -> Guest:
    try:
        return Guest.objects.get(pk=guest_id)
    except Guest.DoesNotExist:
        raise GraphQLError(f"Guest with `id` {guest_id} was not found")


def get_podcast(podcast_id: str | int) -> Podcast:
    try:
        return Podcast.objects.get(pk=podcast_id)
    except Podcast.DoesNotExist:
        raise GraphQLError(f"Podcast with `id` {podcast_id} was not found")


def get_event_image(event_image_id: str | int) -> EventImage:
    try:
        return EventImage.objects.get(pk=event_image_id)
    except EventImage.DoesNotExist:
        raise GraphQLError(f"EventImage with `id` {event_image_id} was not found")


def get_event(event_id: str | int) -> Event:
    try:
        return Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise GraphQLError(f"Event with `id` {event_id} was not found")


def create_host(user_id: int | str, podcast: Podcast) -> Host :
    if not podcast: raise ValueError("podcast is required")
    user = get_user(user_id)
    return Host.objects.create(user=user, podcast=podcast)
