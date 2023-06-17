"""
Contains all mutation functions and methods for a Guest
"""
import graphene
from podcast.models import Guest
from graphql import GraphQLError
from podcast.graphql.utils.general import validate_staff, get_guest
from common.utils import get_organization


def perform_guest_update(info:graphene.ResolveInfo, **kwargs) -> Guest:
    """
    Performs update operation on guest object.
    """
    if not info: raise ValueError("info is required")
    validate_staff(info)

    guest_id = kwargs.get("guest_id")
    organization_id = kwargs.get("organization_id")
    assert guest_id, "guest_id is required"
    if not guest_id: raise GraphQLError("guest_id is required")

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

    if not info: raise ValueError("info is required")
    validate_staff(info)
    organization_id = kwargs.get("organization_id")

    guest = Guest.objects.create(
        name=kwargs.get("name"),
        description=kwargs.get("description"),
        organization=get_organization(organization_id) if organization_id else None
        )
    return guest
