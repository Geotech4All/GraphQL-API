import graphene
from graphql import GraphQLError

from blog.models import Post #type: ignore
from .types import PostType

class BlogQuery(graphene.ObjectType):
    get_post_by_id = graphene.Field(
        PostType,
        post_id=graphene.ID(required=True))
    all_posts = graphene.List(PostType)

    def resolve_all_posts(root, info, **kwargs):
        return Post.objects.all()

    def resolve_get_post_by_id(root, info, **kwargs):
        try:
            return Post.objects.get(pk=kwargs.get('post_id'))
        except Post.DoesNotExist:
            raise GraphQLError("Post with the specified id was not found")
