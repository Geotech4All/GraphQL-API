import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from assets.models import Tag

from opportunities.graphql.types import OpportunityType
from opportunities.models import Opportunity


class OpportunityQueries(graphene.ObjectType):
    opportunities = DjangoFilterConnectionField(OpportunityType)
    opportunity = graphene.Field(OpportunityType, opportunity_id=graphene.ID(required=True))

    def resolve_opportunities(root, info, **kwargs):
        return Opportunity.objects.all()

    def resolve_opportunity(root, info, **kwargs):
        try:
            return Opportunity.objects.get(id=kwargs.get("opportunity_id"))
        except Opportunity.DoesNotExist:
            raise GraphQLError("Specified opportunity was not found")
