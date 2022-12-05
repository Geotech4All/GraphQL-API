import graphene #type: ignore
from graphene_django import DjangoObjectType #type: ignore
from blog.models import Post, Comment
from users.graphql.types import UserType
 

class CommentType(DjangoObjectType):
    author = graphene.Field(UserType)
    class Meta:
        model = Comment
        fields = ("author", "post", "date_added")

    def resolve_author(self, info):
        return self.author
                    
                   
class PostType(DjangoObjectType):
    comments = graphene.List(CommentType)
    class Meta:
        model = Post
        fields = (
            "id", "author",
            "title", "abstract",
            "body", "likes", "dislikes",
            "read_length", "date_added",
            "last_updated"
        )

    def resolve_comments(self, info):
        comments = Comment.objects.filter(post=self)
        return comments
