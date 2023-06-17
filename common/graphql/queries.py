import graphene
from graphene_django.filter import DjangoFilterConnectionField

from common.graphql.types import LocationType, OrganizationType
from common.models import Location, Organization


class CommonQueries(graphene.ObjectType):
    organizations = DjangoFilterConnectionField(OrganizationType)
    organization = graphene.Field(OrganizationType, organization_id=graphene.ID(required=True))
    locations = DjangoFilterConnectionField(LocationType)
    location = graphene.Field(LocationType, location_id=graphene.ID(required=True))

    def resolve_organizations(root, info, **kwargs):
        return Organization.objects.all()

    def resolve_organization(root, info, **kwargs):
        organization_id = kwargs.get("organization_id")
        return Location.objects.get(organization_id)

    def resolve_locations(root, info, **kwargs):
        return Location.objects.all()

    def resolve_location(root, info, **kwargs):
        location_id = kwargs.get("location_id")
        return Location.objects.get(location_id)
