import graphene
from graphene_django import DjangoObjectType
from assets.graphql.types import TagType


from opportunities.models import Opportunity

class OpportunityType(DjangoObjectType):
    opportunity_id = graphene.ID()
    tags = graphene.List(TagType);

    class Meta:
        model = Opportunity
        fields = ("title", "content", "description", "tags", "date_added", "location", "last_updated")
        filter_fields = {"tags__id": ["in"], "location__id": ["exact"]}
        interfaces = (graphene.relay.Node, )


    def resolve_opportunity_id(self, _):
        if isinstance(self, Opportunity):
            return self.pk
        return None

    def resolve_tags(self, _):
        if isinstance(self, Opportunity):
            print(self.tags)
            return self.tags
        return None
