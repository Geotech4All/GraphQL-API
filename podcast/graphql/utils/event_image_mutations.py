"""
Contains all mutation functions and methods on an EventImage
"""
import graphene
from podcast.models import EventImage
from graphql import GraphQLError
from podcast.graphql.utils.general import validate_staff, get_event, get_event_image, get_address


def perform_event_image_update(info: graphene.ResolveInfo, **kwargs) -> EventImage:
    """
    Performs update operation on EventImage.
    """
    if not info: raise ValueError("info is required")
    validate_staff(info)

    event_id = kwargs.get("event_id")
    event_image_id = kwargs.get("event_image_id")

    if not event_image_id: raise GraphQLError("event_image_id is required")
    if not event_id: raise GraphQLError("event_id is required")

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
    if not info: raise ValueError("info is required")
    validate_staff(info)
    event_id = kwargs.get("event_id")
    
    if not event_id: raise GraphQLError("event_id is required")

    event_image = EventImage.objects.create(
        image=kwargs.get("image"),
        event=get_event(event_id),
        description=kwargs.get("description"))
    return event_image
