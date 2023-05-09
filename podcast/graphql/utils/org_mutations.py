"""
Contains all mutation functions and methods for an Organization
"""
import graphene
from podcast.models import Organization
from graphql import GraphQLError
from podcast.graphql.utils.general import validate_staff, get_organization, get_address

def perform_organization_update(info:graphene.ResolveInfo, **kwargs) -> Organization:
    """
    Performs update operation on organization object.
    """
    if not info: raise ValueError("info is required")
    validate_staff(info)

    organization_id = kwargs.get('organization_id', None)
    address_id = str(kwargs.get('address_id'))

    if not organization_id: raise GraphQLError("organization_id is required")

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

