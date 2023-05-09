"""
Contains all mutation functions and methods on an Event
"""
import graphene
from podcast.models import Event
from graphql import GraphQLError
from podcast.graphql.utils.general import validate_staff, get_event, get_organization, get_address


def perform_event_update(info: graphene.ResolveInfo, **kwargs) -> Event:
    """
    Performs update operation on Event.
    """
    if not info: raise ValueError("info is required")
    validate_staff(info)

    event_id = kwargs.get("event_id")
    organizer_id = kwargs.get("organizer_id")
    address_id = kwargs.get("address_id")

    if not event_id: raise GraphQLError("event_id is required")

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
    if not info: raise ValueError("info is required")
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

