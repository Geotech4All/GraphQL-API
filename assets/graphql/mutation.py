import graphene
from graphene_django.types import ErrorType
from graphene_file_upload.scalars import Upload
from graphql_auth.decorators import login_required

from assets.graphql.types import ImageType, TagType
from assets.graphql.utils.image_utils import perform_image_create, perform_image_delete, perform_image_update
from assets.graphql.utils.tag_utils import perform_tag_create, perform_tag_update

class FoldersEnum(graphene.Enum):
    PROFILE = "PROFILE",
    OPPORTUNITY = "OPPORTUNITY"
    BLOG = "BLOG"

class ImageCreateUpdateMutation(graphene.Mutation):
    image = graphene.Field(ImageType)
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    
    class Arguments:
        image_id = graphene.ID()
        image = Upload()
        description = graphene.String()
        folder = FoldersEnum()


    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        image_id = kwargs.get("image_id")
        if image_id:
            updated = perform_image_update(info, **kwargs)
            return ImageCreateUpdateMutation(image=updated, success=True)
        image = perform_image_create(info, **kwargs)
        return ImageCreateUpdateMutation(image=image, success=True)


class ImageDeleteMutation(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)

    class Arguments:
        image_id = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        success = perform_image_delete(info, **kwargs)
        return ImageDeleteMutation(success=success)


class CreateUpdateTagMutation(graphene.Mutation):
    tag = graphene.Field(TagType)
    errors = graphene.List(ErrorType)
    success = graphene.Boolean()

    class Arguments:
        tag_id = graphene.ID()
        title = graphene.String()
        description = graphene.String()
        category = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        if kwargs.get("tag_id"):
            updated_tag = perform_tag_update(info, **kwargs)
            return CreateUpdateTagMutation(tag=updated_tag, success=True)
        new_tag = perform_tag_create(info, **kwargs)
        return CreateUpdateTagMutation(tag=new_tag, success=True)


class AssetMutations(graphene.ObjectType):
    create_update_image = ImageCreateUpdateMutation.Field()
    create_update_tag = CreateUpdateTagMutation.Field()
    delete_image = ImageDeleteMutation.Field()
