from types import FunctionType
import graphene
from graphql import GraphQLError

from users.models import Staff

def staff_required(func):
    def wrapper(root, info, **kwargs):
        # info: graphene.ResolveInfo = kwargs.get("info", None)
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be authenticated to perform this action")
        try:
            Staff.objects.get(user=info.context.user)
            func(root, info, **kwargs)
        except Staff.DoesNotExist:
            raise GraphQLError("You are not permited to perform this action")
    return wrapper
