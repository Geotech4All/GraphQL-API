import graphene
from users.graphql.query import UsersQuery
from users.graphql.mutations import AuthMutations
from blog.graphql.query import BlogQuery
from blog.graphql.mutations import BlogMutations
from podcast.graphql.mutations import PodcastMutations


class Query(
    UsersQuery,
    BlogQuery,
    graphene.ObjectType):
    pass

class Mutation(
        AuthMutations,
        BlogMutations,
        PodcastMutations,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
