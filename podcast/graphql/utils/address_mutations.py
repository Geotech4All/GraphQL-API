"""
Contains all mutation functions and methods for an Address
"""
import graphene
from podcast.models import Address
from graphql import GraphQLError
from podcast.graphql.utils.general import validate_staff, get_address

def perform_address_update(info:graphene.ResolveInfo, **kwargs) -> Address:
    """
    Performs an update operation on address object.
    """
    address_id = kwargs.get('address_id', None)
    assert info, "info is required"
    assert address_id, "address_id is required"
    if not info: raise ValueError("info is required")
    if not address_id: raise GraphQLError("address_id is required")
    validate_staff(info)
    address: Address = get_address(address_id)
    address.city = kwargs.get('city', address.city)
    address.state = kwargs.get('state', address.state)
    address.country = kwargs.get('country', address.country)
    address.address = kwargs.get('address', address.address)
    address.zip_code = kwargs.get('zip_code', address.zip_code)
    address.save()
    return address

def perform_address_create(info:graphene.ResolveInfo, **kwargs) -> Address:
    """
    Performs create operation on address object.
    """
    if not info: raise ValueError("info is required")
    validate_staff(info)
    address: Address = Address.objects.create(
        city=kwargs.get('city'),
        state=kwargs.get('state'),
        country=kwargs.get('country'),
        address=kwargs.get('address'),
        zip_code=kwargs.get('zip_code')
        )
    return address


