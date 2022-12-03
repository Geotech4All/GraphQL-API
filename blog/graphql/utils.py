from typing import Dict
import graphene #type: ignore
from graphql import GraphQLError #type: ignore
from users.models import Staff
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


def perform_blog_update(post_id:str, info:graphene.ResolveInfo, **kwargs: Dict[PostCoreInputs, str]) -> Post:
    """
    Performs update action for a blog post

    :param str blog_id: the `id` of the target post to be updated
    :param graphene.ResolveInfo info: graphene_django info object containig the context
    """

    try:
        post: Post = Post.objects.get(pk=post_id)

        try:
            staff: Staff = Staff.objects.get(user=info.context.user)
            if staff.can_create_post and staff.user == post.author:
                post.author = staff.user
                post.title = kwargs.get('title', post.title)
                post.abstract = kwargs.get('abstract', post.abstract)
                post.body = kwargs.get('body', post.body)
                post.save()
                return post
            else:
                raise GraphQLError("You don not have permisions to alter post")
        except Staff.DoesNotExist:
            raise GraphQLError("You do not have permisions to edit this post")

    except Post.DoesNotExist:
        raise GraphQLError(f"blog post with id {post_id} was not found")


def perform_blog_create(info:graphene.ResolveInfo, **kwargs: Dict[PostCoreInputs, str]) -> Post:
    """
    Performs create action for a blog post
    """

    try:
        staff: Staff = Staff.objects.get(user=info.context.user)
        if staff.can_create_post:
            post: Post = Post.objects.create(
                title=kwargs.get('title'),
                body=kwargs.get('body'),
                abstract=kwargs.get('abstract'),
                author=staff.user)
            post.save()
            return post
        else:
            raise GraphQLError('You do not have permisions to create posts')
    except Staff.DoesNotExist:
        raise GraphQLError(f'You do not have permisions to create posts')
