from django.contrib.auth import get_user_model
import graphene
from graphql import GraphQLError
from podcast.models import (
    Host,
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


def create_host(user_id: int | str, podcast: Podcast) -> Host :
    if not podcast: raise ValueError("podcast is required")
    user = get_user(user_id)
    return Host.objects.create(user=user, podcast=podcast)
