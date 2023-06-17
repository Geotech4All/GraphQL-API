import graphene
from graphene_django.types import DjangoObjectType

from common.models import Location, Organization


class OrganizationType(DjangoObjectType):
    organization_id = graphene.ID()
    class Meta:
        model = Organization
        fields = ("name", "description", "logo")
        filter_fields = {"name": ["exact", "iexact"]}
        interfaces = (graphene.relay.Node, )

    def resolve_organization_id(self):
        if isinstance(self, Organization):
            return self.pk
        return None


class LocationType(DjangoObjectType):
    location_id = graphene.ID()
    class Meta:
        model = Location
        fields = ("country", "state", "address", "zip_code", "date_added", "last_updated")
        filter_fields = {"country": ["exact", "iexact"]}
        interfaces = (graphene.relay.Node, )

    def resolve_location_id(self):
        if isinstance(self, Location):
            return self.pk
        return None
