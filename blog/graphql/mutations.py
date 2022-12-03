import graphene #type: ignore
from graphene_django.types import ErrorType #type: ignore
from graphql_auth.decorators import login_required #type: ignore
from .types import CommentType, PostType
from .utils import PostCoreInputs, perform_blog_create, perform_blog_update
from blog.models import Comment, Post


class PostCreateUpdateMutation(graphene.Mutation):
    """
    Performs create and update functionality on a blog postself.
    To perform an update, you just need to pass in the blog `id`.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    post = graphene.Field(PostType)

    class Arguments:
        """
        Core inputs required for creating a blog post
        """
        title = graphene.String(
            required=True,
            description="The post title")
        abstract = graphene.String(
            description="A short description of this post")
        body = graphene.String(
            required=True,
            description="Tho post contents")
        post_id = graphene.ID(
            required=False,
            description="The `id` of the blog post you want to update")

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        post_id = kwargs.get('post_id')
        if post_id:
            post = perform_blog_update(post_id, info, **kwargs)
            return PostCreateUpdateMutation(success=True, post=post)
        post = perform_blog_create(info, **kwargs)
        return PostCreateUpdateMutation(success=True, post=post)


class CommentCreateMutation(graphene.Mutation):
    """
    Handles create operarion for comments
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    comment = graphene.Field(CommentType)

    class Arguments:
        post_id = graphene.ID(
            required=True,
            description="The `id` of the post to which this comment belongs.")
        body = graphene.String(
            required=True,
            description="The contents of the comment")

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        post_id = kwargs.get('post_id', None)
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.create(
            post=post,
            body=kwargs.get('body'),
            author=info.context.user)
        return CommentCreateMutation(comment=comment, success=True)

class BlogMutations(graphene.ObjectType):
    create_update_post = PostCreateUpdateMutation.Field()
    create_comment = CommentCreateMutation.Field()
