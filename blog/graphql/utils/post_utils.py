from typing import Dict
import graphene #type: ignore
from graphql import GraphQLError
from assets.utils import get_image
from blog.graphql.utils.common import get_post_by_id
from users.graphql.utils.staff_utils import validate_and_return_staff
from blog.models import Post


class PostCoreInputs:
    """
    Core inputs required for creating a blog post
    """
    author_id = graphene.ID(
        required=True,
        description="The `id` of the user trying to create this post")
    title = graphene.String(
        required=True,
        description="The post title")
    abstract = graphene.String(
        description="A short description of this post")
    body = graphene.String(
        required=True,
        description="Tho post contents")


def perform_post_update(info:graphene.ResolveInfo, **kwargs: Dict[PostCoreInputs, str]) -> Post:
    """
    Performs update action for a blog post if the user is authorized

    :param str blog_id: the `id` of the target post to be updated
    :param graphene.ResolveInfo info: graphene_django info object containig the context
    """

    post_id = kwargs.get("post_id")
    if not post_id:
        raise GraphQLError("post_id is required")

    post = get_post_by_id(str(post_id))
    staff = validate_and_return_staff(info)

    if not (staff.can_alter_post or staff.user.is_superuser or post.author == staff.user):
        raise GraphQLError("You don not have permisions to alter this post")

    post.author = staff.user
    if kwargs.get("title", None): post.title = kwargs.get("title")
    if kwargs.get('abstract', None): post.abstract = kwargs.get('abstract')
    if kwargs.get('body', None): post.body = kwargs.get('body')
    cover_photo_id = kwargs.get("cover_photo_id", None)
    if cover_photo_id is not None:
        image = get_image(str(cover_photo_id))
        post.cover_photo = image
    post.save()
    return post

def perform_post_create(info:graphene.ResolveInfo, **kwargs: Dict[PostCoreInputs, str]) -> Post:
    """
    Performs create action for a blog post if the user is authorized
    """

    staff = validate_and_return_staff(info)

    if not (staff.can_create_post or staff.user.is_superuser):
        raise GraphQLError("You are not authorised to create posts")

    cover_photo_id = kwargs.get("cover_photo_id", None)
    image = get_image(str(cover_photo_id)) if cover_photo_id is not None else None;
    post: Post = Post.objects.create(
        title=kwargs.get('title'),
        body=kwargs.get('body'),
        abstract=kwargs.get('abstract'),
        author=staff.user,
        cover_photo=image)
    post.save()
    return post


def perform_post_delete(info: graphene.ResolveInfo, **kwargs) -> bool:
    """
    Performs post deletion if the user is authorized
    """
    post_id = kwargs.get("post_id")
    if not post_id:
        raise GraphQLError("post_id is required")

    staff = validate_and_return_staff(info)
    post = get_post_by_id(str(post_id))
    if not (staff.can_delete_post or staff.user.is_superuser or post.author == staff.user):
        raise GraphQLError("You are not authorized to delete this post")

    deleted = post.delete()
    return len(deleted) > 0
