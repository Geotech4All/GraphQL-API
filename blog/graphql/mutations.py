import graphene #type: ignore
from graphene_django.types import ErrorType
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError #type: ignore
from graphql_auth.decorators import login_required

from blog.graphql.utils.post_image_utils import perform_post_image_create #type: ignore
from .types import CommentType, PostImageType, PostType
from .utils.post_utils import perform_post_create, perform_post_delete, perform_post_update
from blog.models import Comment, Post

class PostViewsIncreaseMutation(graphene.Mutation):
    """
    Increases the view count on a post
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    post = graphene.Field(PostType)

    class Arguments:
        post_id = graphene.ID(
            required=True,
            description="The id of the post to be updated")

    @classmethod
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        post_id = kwargs.get("post_id");
        if not post_id:
            raise GraphQLError("post_id is required")
        try:
            post:Post = Post.objects.get(pk=post_id)
            post.views = post.views + 1
            post.save()
            return PostViewsIncreaseMutation(success=True, post=post)
        except Post.DoesNotExist:
            raise GraphQLError(f"post with id {post_id} was not found")


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
        cover_photo_id = graphene.ID(description="The id of the associated image")

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        post_id = kwargs.get('post_id')
        if post_id:
            post = perform_post_update(info, **kwargs)
            return PostCreateUpdateMutation(success=True, post=post)
        post = perform_post_create(info, **kwargs)
        return PostCreateUpdateMutation(success=True, post=post)


class PostDeleteMutation(graphene.Mutation):
    """
    Deletes a post with the specified id.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)

    class Arguments:
        post_id = graphene.ID(
            required=True,
            description="The id of the post to be deleted")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        deleted = perform_post_delete(info, **kwargs)
        return PostDeleteMutation(success=deleted)


class PostImageCreateUpdateMutation(graphene.Mutation):
    """
    Create and update mutation for a post image.
    To perform an update, all you need to do is pass in the post image `id`
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    post_image = graphene.Field(PostImageType)

    class Arguments:
        image = Upload(description="The image file")
        description = graphene.String(description="this can be used as the `alt` property of the image")

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        post_image = perform_post_image_create(info, **kwargs)
        print(post_image)
        return PostImageCreateUpdateMutation(success=True, post_image=post_image)


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
        try:
            post:Post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("A post with the specified `id` DoesNotExist")
        comment = Comment.objects.create(
            post=post,
            body=kwargs.get('body'),
            author=info.context.user)
        return CommentCreateMutation(comment=comment, success=True)

class BlogMutations(graphene.ObjectType):
    create_update_post = PostCreateUpdateMutation.Field()
    delete_post = PostDeleteMutation.Field()
    create_comment = CommentCreateMutation.Field()
    create_update_post_image = PostImageCreateUpdateMutation.Field()
    increase_post_view_count = PostViewsIncreaseMutation.Field()
