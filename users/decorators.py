from collections.abc import Callable
import graphene
from graphql import GraphQLError

from users.models import Staff

def ensure_logged_in(info: graphene.ResolveInfo):
    if not info.context.user.is_authenticated:
        raise GraphQLError("You must be authenticated to perform this action")

def staff_required(func):
    def wrapper(root, info, **kwargs):
        ensure_logged_in(info)
        try:
            Staff.objects.get(user=info.context.user)
            func(root, info, **kwargs)
        except Staff.DoesNotExist:
            raise GraphQLError("You are not permited to perform this action")
    return wrapper

def my_login_required(func):
    def wrapper(root, info: graphene.ResolveInfo, **kwargs):
        ensure_logged_in(info)
        func(root, info, **kwargs)
    return wrapper
