import graphene
from enum import Enum
from graphene_django.types import ErrorType
from graphql_auth.decorators import login_required
from .types import AddressType
from .utils import perform_address_create, perform_address_update


class AddressCreateUpdateMutation(graphene.Mutation):
    """
    Performs create and update activity on an `Address`.
    To perform an update all you need to do is pass in the address `id`.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    address = graphene.Field(AddressType)

    class Arguments:
        address_id = graphene.ID(description="The `id` of the address to be updated")
        city = graphene.String(required=True)
        state = graphene.String(required=True)
        country = graphene.String(required=True)
        address = graphene.String(required=True)
        zip_code = graphene.String()


    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        address_id = kwargs.get('address_id')
        if address_id:
            address = perform_address_update(address_id, info=info, **kwargs)
            return AddressCreateUpdateMutation(success=True, address=address)
        address = perform_address_create(info, **kwargs)
        return AddressCreateUpdateMutation(success=True, address=address)


class PodcastMutations(graphene.ObjectType):
    create_update_address = AddressCreateUpdateMutation.Field()
