import graphene #type: ignore
from .types import PostType

class BlogQuery(graphene.ObjectType):
    all_posts = graphene.List(PostType)
