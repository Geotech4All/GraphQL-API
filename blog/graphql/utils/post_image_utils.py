import graphene
from graphql import GraphQLError

from users.graphql.utils.staff_utils import validate_and_return_staff
from blog.models import PostImage


def perform_post_image_create(info: graphene.ResolveInfo, **kwargs) -> PostImage:
    staff = validate_and_return_staff(info)
    if staff.can_create_post:
        return PostImage.objects.create(image=kwargs.get("image"), description=kwargs.get("description"))
    raise GraphQLError("You are not permited to perform this action")
