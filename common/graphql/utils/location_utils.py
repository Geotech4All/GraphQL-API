import graphene
from graphql import GraphQLError
from common.models import Location, Organization
from common.utils import get_location

from users.graphql.utils.staff_utils import validate_and_return_staff


def perform_location_update(info: graphene.ResolveInfo, **kwargs) -> Location:
    validate_and_return_staff(info)
    location_id = kwargs.get("location_id")
    assert location_id, GraphQLError("location_id is required for location_id")

    location = get_location(location_id)

    country = kwargs.get("country")
    state = kwargs.get("state")
    address = kwargs.get("address")
    zip_code = kwargs.get("zip_code")

    if country: location.country = country
    if state: location.state = state
    if address: location.address = address
    if zip_code: location.zip_code = zip_code

    location.save()
    return location


def perform_location_create(info: graphene.ResolveInfo, **kwargs) -> Organization:
    validate_and_return_staff(info)
    return Organization.objects.create(
        country=kwargs.get("country"),
        state=kwargs.get("state"),
        address=kwargs.get("address"),
        zip_code=kwargs.get("zip_code")
    )
