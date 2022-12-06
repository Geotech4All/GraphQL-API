import graphene
from graphql import GraphQLError
from podcast.models import Address, Organization
from users.models import Staff

def validate_staff(info: graphene.ResolveInfo):
    try:
        Staff.objects.get(user=info.context.user)
    except Staff.DoesNotExist:
        raise GraphQLError("You are not authorised to perform this action")

def perform_address_update(info:graphene.ResolveInfo, **kwargs) -> Address:
    """
    Performs an update operation on address object.
    """
    address_id = kwargs.get('address_id', None)
    if not address_id:
        raise GraphQLError("address_id is required")
    try:
        validate_staff(info)
        address: Address = Address.objects.get(pk=address_id)
        address.city = kwargs.get('city', address.city)
        address.state = kwargs.get('state', address.state)
        address.country = kwargs.get('country', address.country)
        address.address = kwargs.get('address', address.address)
        address.zip_code = kwargs.get('zip_code', address.zip_code)
        address.save()
        return address
    except Address.DoesNotExist:
        raise GraphQLError("Address with the specified `id` does not exist.")

def perform_address_create(info:graphene.ResolveInfo, **kwargs) -> Address:
    """
    Performs create operation on address object.
    """
    validate_staff(info)
    address: Address = Address.objects.create(
        city=kwargs.get('city'),
        state=kwargs.get('state'),
        country=kwargs.get('country'),
        address=kwargs.get('address'),
        zip_code=kwargs.get('zip_code')
        )
    return address

def get_address(address_id: str | int) -> Address:
    try:
        return Address.objects.get(pk=address_id)
    except Address.DoesNotExist:
        raise GraphQLError("Address with the specified `id` was not found")

def perform_organization_update(info:graphene.ResolveInfo, **kwargs) -> Organization:
    """
    Performs update operation on organization object.
    """
    organization_id = kwargs.get('organization_id', None)
    address_id = str(kwargs.get('address_id'))
    if organization_id:
        try:
            validate_staff(info)
            organization: Organization = Organization.objects.get(pk=organization_id)
            organization.name = kwargs.get('name')
            organization.address = get_address(address_id) if address_id else organization.address
            organization.description = kwargs.get('organization', organization.description)
            organization.logo = kwargs.get('logo', organization.logo)
            organization.email = kwargs.get('email', organization.email)    
            organization.phone = kwargs.get('phone', organization.phone)    
            organization.save()
            return organization
        except Organization.DoesNotExist:
                raise GraphQLError("Organization with the specified `id` was not found")
    else:
        raise GraphQLError("organization_id is required")

def perform_organization_create(info:graphene.ResolveInfo, **kwargs) -> Organization:
    """
    Performs create operation on organization object.
    """
    address_id = str(kwargs.get('address_id'))
    try:
        validate_staff(info)
        organization: Organization = Organization.objects.get(pk=organization_id)
        organization.name = kwargs.get('name')
        organization.address = get_address(address_id) if address_id else organization.address
        organization.description = kwargs.get('organization', organization.description)
        organization.logo = kwargs.get('logo', organization.logo)
        organization.email = kwargs.get('email', organization.email)    
        organization.phone = kwargs.get('phone', organization.phone)    
        organization.save()
        return organization
    except Organization.DoesNotExist:
            raise GraphQLError("Organization with the specified `id` was not found")

