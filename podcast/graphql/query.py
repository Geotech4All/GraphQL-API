import graphene
from graphql.error import GraphQLError
from podcast.graphql.types import AddressNode
from podcast.models import Address

class PodcastQuery(graphene.ObjectType):
    get_address_by_id = graphene.Field(
            AddressNode,
            address_id=graphene.ID(required=True))


    def resolve_get_address_by_id(root, info, **kwargs):
        address_id = kwargs.get('address_id')
        try:
            return Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            raise GraphQLError("The specified address was not found")
