from types import FunctionType
import graphene
from graphql import GraphQLError

from users.models import Staff

def staff_required(func):
    def wrapper(self, info: graphene.ResolveInfo, *args, **kwargs):
        try:
            Staff.objects.get(user=info.context.user)
            func(self, info, *args, **kwargs)
        except Staff.DoesNotExist:
            raise GraphQLError("You are not permited to perform this action")
    return wrapper
