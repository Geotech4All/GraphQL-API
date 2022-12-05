from django_countries.graphql.types import Country
import graphene
from podcast.models import Address


class AddressType(graphene.ObjectType):
    """
    Address graphql of object type
    """
    country = graphene.Field(Country)
    class Meta:
        model = Address
        fields = (
            "city",
            "state",
            "country",
            "address",
            "zip_code",
            "date_added",
            "last_updated")
                   
