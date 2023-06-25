from datetime import datetime, timedelta
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from assets.models import Tag

from opportunities.graphql.types import OpportunityType
from opportunities.models import Opportunity

class OpportunityDates(graphene.Enum):
    Today = datetime.today()
    ThisWeek = datetime.today() - timedelta(days=7)
    ThisMonth = datetime.today() - timedelta(days=30)
    ThisYear = datetime.today() - timedelta(days=365)
    AnyTime = None

class OpportunityQueries(graphene.ObjectType):
    opportunities = DjangoFilterConnectionField(OpportunityType, date_posted=OpportunityDates())
    opportunity = graphene.Field(OpportunityType, opportunity_id=graphene.ID(required=True))

    def resolve_opportunities(root, info, **kwargs):
        date_posted: OpportunityDates = OpportunityDates(kwargs.get("date_posted") or None)
        if date_posted:
            match(date_posted):
                case OpportunityDates.Today:
                    return Opportunity.objects.filter(last_updated__gte=OpportunityDates.Today)
                case OpportunityDates.ThisWeek:
                    return Opportunity.objects.filter(last_updated__gte=OpportunityDates.ThisWeek)
                case OpportunityDates.ThisMonth:
                    return Opportunity.objects.filter(last_updated__gte=OpportunityDates.ThisMonth)
                case OpportunityDates.ThisYear:
                    return Opportunity.objects.filter(last_updated__gte=OpportunityDates.ThisYear)
                case OpportunityDates.AnyTime:
                    return Opportunity.objects.all()
        return Opportunity.objects.all()

    def resolve_opportunity(root, info, **kwargs):
        try:
            return Opportunity.objects.get(id=kwargs.get("opportunity_id"))
        except Opportunity.DoesNotExist:
            raise GraphQLError("Specified opportunity was not found")
