"""
Contains all mutation functions and methods on a Podcast
"""
import graphene
from assets.utils import get_file, get_image
from podcast.models import Podcast
from graphql import GraphQLError
from podcast.graphql.utils.general import create_host, get_guest, get_podcast
from users.graphql.utils.staff_utils import validate_and_return_staff

podcast_fields = ["host_ids", "guest_ids", "title", "description", "audio_id", "cover_photo_id"]

def perform_podcast_update(info: graphene.ResolveInfo, **kwargs) -> Podcast:
    """
    Performs update operation on Podcast if the user is authorized
    """
    staff = validate_and_return_staff(info)
    if not (staff.can_alter_podcast or staff.user.is_superuser):
        raise GraphQLError("You are not authorized to alter this podacast")

    podcast_id = kwargs.get("podcast_id", None)
    assert podcast_id is not None, GraphQLError("podcast_id is requred for podcast update")
    podcast = get_podcast(podcast_id)

    for field in podcast_fields:
        field_value = kwargs.get(field, None)
        if field_value is not None:
            if field == "host_ids":
                assert len(field_value) > 0, GraphQLError("A podcast must have at least one host")
                for id in field_value: create_host(id, podcast)
            elif field == "guest_ids":
                for id in field_value: podcast.guests.add(get_guest(id))
            elif field == "audio_id":
                podcast.audio = get_file(id=str(field_value))
            elif field == "cover_photo_id":
                podcast.cover_photo = get_image(id=str(field_value))
            else:
                if hasattr(Podcast, field): setattr(podcast, field, field_value)
    return podcast


def perform_podcast_create(info: graphene.ResolveInfo, **kwargs) -> Podcast:
    """
    Performs create operation on Podcast if the user is authorized
    """
    if not info: raise ValueError("info is required")

    staff = validate_and_return_staff(info)
    if not (staff.user.is_superuser or staff.can_create_podcast):
        raise GraphQLError("You are not authirized create a podcast")

    title = kwargs.get("title", None)
    description = kwargs.get("description", None)
    host_ids = kwargs.get("host_ids", None)
    guest_ids = kwargs.get("guest_ids", None)
    audio_id = kwargs.get("audio_id", None)
    cover_photo_id = kwargs.get("cover_photo_id", None)
    assert title is not None, GraphQLError("title is required for podcast creation")
    assert description is not None, GraphQLError("description is requred for podcast creation")
    assert host_ids is not None and len(host_ids) > 0, GraphQLError("A podcast must have a host")
    assert audio_id is not None, GraphQLError("A podcast must have an associated audio file")

    podcast: Podcast = Podcast.objects.create(title=title, description=description)

    for id in host_ids: create_host(id, podcast)
    if guest_ids is not None:
        for id in guest_ids:
            podcast.guests.add(get_guest(id))
    podcast.audio = get_file(str(audio_id))
    if cover_photo_id: podcast.cover_photo = get_image(str(cover_photo_id))

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

