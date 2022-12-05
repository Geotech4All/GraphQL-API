import graphene

from blog.models import Post #type: ignore
from .types import PostType

class BlogQuery(graphene.ObjectType):
    all_posts = graphene.List(PostType)

    def resolve_all_posts(root, info, **kwargs):
        return Post.objects.all()
