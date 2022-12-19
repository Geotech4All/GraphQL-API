import graphene
from graphene_django import DjangoListField
from graphql_auth.schema import MeQuery, UserQuery

from users.graphql.types import StaffType
from users.decorators import staff_required
from users.models import Staff

class StaffQuery(graphene.ObjectType):
    staff_list = DjangoListField(StaffType)

    @staff_required
    def resolve_staff_list(self, info: graphene.ResolveInfo, **kwargs):
        queryset = Staff.objects.all()
        print(queryset)
        return queryset

class UsersQuery(UserQuery, MeQuery, StaffQuery, graphene.ObjectType):
    pass
