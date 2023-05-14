import graphene
from graphql import GraphQLError
from assets.models import Image
from assets.utils import get_image

from users.graphql.utils.staff_utils import validate_and_return_staff


def perform_image_create(info: graphene.ResolveInfo, **kwargs) -> Image:
    validate_and_return_staff(info)
    
    image = Image.new(image=kwargs.get("image"), folder=kwargs.get("folder"), description=kwargs.get("description"))
    return image

def perform_image_update(info: graphene.ResolveInfo, **kwargs) -> Image:
    validate_and_return_staff(info)
    image_id = kwargs.get("image_id")
    if not image_id:
        raise GraphQLError("image_id is required")

    image = get_image(id=str(image_id))
    return image.update(image=kwargs.get("image"), description=kwargs.get("description"))

def perform_image_delete(info: graphene.ResolveInfo, **kwargs) -> bool:
    validate_and_return_staff(info)
    image = get_image(id=str(kwargs.get("image_id")))
    image.delete()
    return True
