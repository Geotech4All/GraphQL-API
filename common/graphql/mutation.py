import graphene
from graphene_django.types import ErrorType
from graphql_auth.decorators import login_required

from common.graphql.types import LocationType, OrganizationType
from common.graphql.utils.location_utils import perform_location_create, perform_location_update
from common.graphql.utils.organization_utils import perform_organization_create, perform_organization_update


class LocationCreateUpdateMutation(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    location = graphene.Field(LocationType)

    class Arguments:
        location_id = graphene.ID()
        country = graphene.String()
        state = graphene.String()
        address = graphene.String()
        zip_code = graphene.String()


    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        location_id = kwargs.get("location_id")
        if location_id:
            location = perform_location_update(info, **kwargs)
            return LocationCreateUpdateMutation(success=True, location=location)
        location = perform_location_create(info, **kwargs)
        return LocationCreateUpdateMutation(success=True, location=location)


class OrganizationCreateUpdateMutation(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    organization = graphene.Field(OrganizationType)

    class Arguments:
        organization_id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        logo_id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        organization_id = kwargs.get("organization_id")
        if organization_id:
            organization = perform_organization_update(info, **kwargs)
            return OrganizationCreateUpdateMutation(success=True, organization=organization)
        organization = perform_organization_create(info, **kwargs)
        return OrganizationCreateUpdateMutation(success=True, organization=organization)


class CommonMutation(graphene.ObjectType):
    create_update_location = LocationCreateUpdateMutation.Field()
    create_update_organization = OrganizationCreateUpdateMutation.Field()
