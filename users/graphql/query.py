import graphene
from graphene_django import DjangoListField
from graphql_auth.decorators import login_required
from graphql_auth.schema import MeQuery, UserQuery

from users.graphql.types import ProfileType, StaffType
from users.decorators import my_login_required, staff_required
from users.graphql.utils import get_object_or_errror
from users.models import Profile, Staff

class StaffQuery(graphene.ObjectType):
    staff_list = DjangoListField(StaffType)
    user_profile = graphene.Field(ProfileType, user_id=graphene.ID(required=True))

    @staff_required
    def resolve_staff_list(self, info: graphene.ResolveInfo, **kwargs):
        queryset = Staff.objects.all()
        return queryset

    @classmethod
    @login_required
    def resolve_user_profile(cls, root, info, **kwargs):
        user_id = kwargs.get("user_id")
        profile = get_object_or_errror(Profile, user__id=user_id)
        return profile

class UsersQuery(UserQuery, MeQuery, StaffQuery, graphene.ObjectType):
    pass
