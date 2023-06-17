from graphql import GraphQLError
from common.models import Location, Organization


def get_organization(id: int|str) -> Organization:
    """
    Get's an Organization or throws a GraphQLError if not found
    """
    try:
        return Organization.objects.get(id=id)
    except Organization.DoesNotExist:
        raise GraphQLError(f"Organization with id {id} was not found")


def get_location(id: int|str) -> Location:
    """
    Get's a Location or throws a GraphQLError if not found
    """
    try:
        return Location.objects.get(id=id)
    except Location.DoesNotExist:
        raise GraphQLError(f"Location with id {id} was not found")
