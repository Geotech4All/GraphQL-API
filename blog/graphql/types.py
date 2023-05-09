import graphene #type: ignore
from graphene_django import DjangoObjectType #type: ignore
from blog.models import Post, Comment, PostImage
from users.graphql.types import UserType
 

class PostImageType(DjangoObjectType):
    post_image_id = graphene.ID()
    image = graphene.String()
    class Meta:
        model = PostImage
        fields = ("description", )
        filter_fields = {"description": ["icontains", "istartswith", "exact"]}
        interfaces = (graphene.relay.Node, )

    def resolve_post_image_id(self, _):
        if isinstance(self, PostImage):
            return self.pk
        return None

    def resolve_image(self, _):
        if isinstance(self, PostImage):
            return self.get_image
        return None

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
