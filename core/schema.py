import graphene
from users.graphql.query import UsersQuery
from users.graphql.mutations import AuthMutations


class Query(UsersQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
