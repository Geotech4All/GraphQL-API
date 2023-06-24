import graphene
from graphene_django.types import ErrorType
from graphql_auth.decorators import login_required

from django.utils.translation import gettext_lazy as _
from opportunities.graphql.types import OpportunityType
from opportunities.graphql.utils.opportunity_utils import (
        perform_opportunity_create,
        perform_opportunity_update)

class OpportunityCreateUpdateMutation(graphene.Mutation):
    """
    Create new or update existing opportunity
    """
    opportunity = graphene.Field(OpportunityType)
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String()
        opportunity_id = graphene.ID()
        # Updates
        tag_ids = graphene.List(graphene.ID)
        description = graphene.String()
        organization_id = graphene.ID()
        location_id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, _, info:graphene.ResolveInfo, **kwargs):
        opportunity_id = kwargs.get("opportunity_id")
        if opportunity_id:
            updated = perform_opportunity_update(info, **kwargs)
            return OpportunityCreateUpdateMutation(opportunity=updated, success=True)
        opportunity = perform_opportunity_create(info, **kwargs)
        return OpportunityCreateUpdateMutation(opportunity=opportunity, success=True)


class OpportunityMutations(graphene.ObjectType):
    create_update_opportunity = OpportunityCreateUpdateMutation.Field()
