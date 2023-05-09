from graphql import GraphQLError
from blog.models import Post


def get_post_by_id(post_id: str | int) -> Post:
    try:
        return Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise GraphQLError(f"blog post with id {post_id} was not found")
