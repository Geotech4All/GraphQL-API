import graphene
from graphene_django import DjangoObjectType


from opportunities.models import Opportunity

class OpportunityType(DjangoObjectType):
    opportunity_id = graphene.ID()
    class Meta:
        model = Opportunity
        fields = ("title", "content", "abstract", "category", "date_added", "last_updated")
        filter_fields = {"category__title": ["icontains", "exact", "istartswith"]}
        interfaces = (graphene.relay.Node, )


    def resolve_opportunity_id(self, _):
        if isinstance(self, Opportunity):
            return self.pk
        return None
