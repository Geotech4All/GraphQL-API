import graphene
from assets.graphql.mutation import AssetMutations
from assets.graphql.query import AssetsQuery
from common.graphql.mutation import CommonMutation
from common.graphql.queries import CommonQueries
from opportunities.graphql.mutations import OpportunityMutations
from opportunities.graphql.queries import OpportunityQueries
from users.graphql.query import UsersQuery
from users.graphql.mutations import AuthMutations
from blog.graphql.query import BlogQuery
from blog.graphql.mutations import BlogMutations
from podcast.graphql.mutations import PodcastMutations
from podcast.graphql.query import PodcastQuery


class Query(
    UsersQuery,
    BlogQuery,
    PodcastQuery,
    AssetsQuery,
    CommonQueries,
    OpportunityQueries,
    graphene.ObjectType):
    pass

class Mutation(
        AuthMutations,
        BlogMutations,
        PodcastMutations,
        AssetMutations,
        CommonMutation,
        OpportunityMutations,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
