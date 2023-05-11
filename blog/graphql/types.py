import graphene #type: ignore
from graphene_django import DjangoObjectType #type: ignore
from blog.models import Post, Comment
from users.graphql.types import UserType
 

class CommentType(DjangoObjectType):
    author = graphene.Field(UserType)
    class Meta:
        model = Comment
        fields = ("author", "post", "date_added")

    def resolve_author(self, _):
        return self.author
                    
                   
class PostType(DjangoObjectType):
    comments = graphene.List(CommentType)
    post_id = graphene.ID()
    class Meta:
        model = Post
        fields = (
            "id", "author",
            "title", "abstract",
            "body", "likes", "dislikes",
            "read_length", "date_added",
            "last_updated", "views", "cover_photo"
        )
        filter_fields = {
            "date_added": ["exact", "icontains", "istartswith"],
            "title": ["exact", "icontains", "istartswith"],
            "body": ["icontains", "istartswith"],
            "read_length": ["exact", "icontains", "istartswith"],
            "likes": ["exact"],
            "dislikes": ["exact"],
        }
        interfaces = (graphene.relay.Node, )

    def resolve_comments(self, _):
        comments = Comment.objects.filter(post=self)
        return comments

    def resolve_post_id(self, _):
        if isinstance(self, Post):
            return self.pk
        return None;
