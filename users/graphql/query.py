import graphene
from graphql_auth.schema import MeQuery, UserQuery


class UsersQuery(
    UserQuery,
    MeQuery,
    graphene.ObjectType):
    pass
