from graphql import GraphQLError
from assets.models import Image


def get_image(id: str|int) -> Image:
    """
    Gets and retuns an image with the specified `id`
    and thows a graphql error if the image was not found
    """
    try:
        return Image.objects.get(pk=id)
    except Image.DoesNotExist:
        raise GraphQLError(f"Image reccord with id {id} was not found")
