import graphene
from graphene_django import DjangoObjectType
from podcast.models import Address, Organization, Guest


class AddressNode(DjangoObjectType):
    """
    Address graphql object type
    """
    class Meta:
        model = Address
        fields = (
            "id",
            "city",
            "state",
            "country",
            "address",
            "zip_code",
            "date_added",
            "last_updated")
                   

class OrganizationType(DjangoObjectType):
    """
    Organization graphql object type
    """
    logo = graphene.String()
    class Meta:
        model = Organization
        fields = ("id", "name", "address", "description", "logo", "email", "phone")

    def resolve_logo(self, info: graphene.ResolveInfo):
        if isinstance(self, Organization):
            return self.get_logo_url()
        return None


class GuestType(DjangoObjectType):
    """
    Guest graphql object type
    """
    class Meta:
        model = Guest
        fields = ("id", "name", "description", "organization")
