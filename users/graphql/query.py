import graphene
from graphql_auth.schema import MeQuery, UserQuery

from users.graphql.types import StaffType
from users.decorators import staff_required
from users.models import Staff


class UsersQuery(UserQuery, MeQuery, graphene.ObjectType):
    get_staff_list = graphene.List(StaffType)

    @staff_required
    def resolve_get_staff_list(self, **_):
        return Staff.objects.all()
