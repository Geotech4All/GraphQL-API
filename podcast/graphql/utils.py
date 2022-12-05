import graphene
from graphql import GraphQLError
from podcast.models import Address
from users.models import Staff


def perform_address_update(address_id: str | int, info:graphene.ResolveInfo, **kwargs) -> Address:
    """
    Performs an update operation on address object.
    """
    try:
        try:
            staff: Staff = Staff.objects.get(user=info.context.user)
            address: Address = Address.objects.get(pk=address_id)
            address.city = kwargs.get('city', address.city)
            address.state = kwargs.get('state', address.state)
            address.country = kwargs.get('country', address.country)
            address.address = kwargs.get('address', address.address)
            address.zip_code = kwargs.get('zip_code', address.zip_code)
            address.save()
            return address
        except Staff.DoesNotExist:
            raise GraphQLError("You do not have permissions to alter this address")
    except Address.DoesNotExist:
        raise GraphQLError("Address with the specified `id` does not exist.")

def perform_address_create(info:graphene.ResolveInfo, **kwargs) -> Address:
    """
    Performs create operation on address object.
    """
    try:
        staff: Staff = Staff.objects.get(user=info.context.user)
        address: Address = Address.objects.create(
            city=kwargs.get('city'),
            state=kwargs.get('state'),
            country=kwargs.get('country'),
            address=kwargs.get('address'),
            zip_code=kwargs.get('zip_code')
            )
        return address
    except Staff.DoesNotExist:
        raise GraphQLError("You do not have permissions to alter this address")
