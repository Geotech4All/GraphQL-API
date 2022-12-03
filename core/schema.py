import graphene
from users.graphql.query import UsersQuery
from users.graphql.mutations import AuthMutations
from blog.graphql.mutations import BlogMutations


class Query(UsersQuery, graphene.ObjectType):
    pass

class Mutation(
        AuthMutations,
        BlogMutations,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
