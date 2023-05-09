"""
Contains all mutation functions and methods on a Podcast
"""
import graphene
from podcast.models import Podcast
from graphql import GraphQLError
from podcast.graphql.utils.general import create_host, get_guest, get_podcast
from users.graphql.utils.staff_utils import validate_and_return_staff


def perform_podcast_update(info: graphene.ResolveInfo, **kwargs) -> Podcast:
    """
    Performs update operation on Podcast if the user is authorized
    """
    if not info: raise ValueError("info is required")

    staff = validate_and_return_staff(info)
    if not (staff.can_alter_podcast or staff.user.is_superuser or staff.can_create_podcast):
        raise GraphQLError("You are not authorized to perform podacast update")
    
    podcast_id = kwargs.get("podcast_id")
    host_ids = kwargs.get("host_ids")
    guest_ids = kwargs.get("guest_ids")
    if not podcast_id: raise GraphQLError("podcast_id is required")

    podcast = get_podcast(podcast_id)
    if host_ids:
        if not len(host_ids) > 0: raise GraphQLError("A podcast must have at least one host")
        for id in host_ids:
            create_host(id, podcast)
    if guest_ids:
        for id in guest_ids:
            podcast.guests.add(get_guest(id))
    podcast.title = kwargs.get("title", podcast.title)
    podcast.description = kwargs.get("description", podcast.description)
    podcast.audio = kwargs.get("audio", podcast.audio)
    podcast.cover_photo = kwargs.get("cover_photo", podcast.cover_photo)
    podcast.save()
    return podcast


def perform_podcast_create(info: graphene.ResolveInfo, **kwargs) -> Podcast:
    """
    Performs create operation on Podcast if the user is authorized
    """
    if not info: raise ValueError("info is required")

    staff = validate_and_return_staff(info)
    if not (staff.can_alter_podcast or staff.user.is_superuser or staff.can_create_podcast):
        raise GraphQLError("You are not authirized to perform podcast creation")

    host_ids = kwargs.get("host_ids")
    guest_ids = kwargs.get("guest_ids")
    podcast = Podcast.objects.create(
        title=kwargs.get("title"),
        listens=0,
        description=kwargs.get("description"),
        audio=kwargs.get("audio"),
        cover_photo=kwargs.get("cover_photo")
        )
    if host_ids:
        if not len(host_ids) > 0: raise GraphQLError("A podcast must have at least one host")
        for id in host_ids:
            create_host(id, podcast)
    if guest_ids:
        for id in guest_ids:
            podcast.guests.add(get_guest(id))
    podcast.save()
    return podcast


def perform_podcast_listens_increase(**kwargs) -> Podcast:
    """
    Increases a podcasts listens by 1 and returns that podcast
    """
    podcast_id = kwargs.get("podcast_id")
    assert podcast_id, GraphQLError("podcast_id is required")
    if not podcast_id: raise GraphQLError("podcast_id is required")
    podcast = get_podcast(str(podcast_id))
    podcast.listens += 1
    podcast.save()
    return podcast

