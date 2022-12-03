import graphene #type: ignore
from graphene_django import DjangoObjectType #type: ignore
from blog.models import Post, Comment
 

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("author", "post", "date_added")
                    
                   
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
