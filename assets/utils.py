from graphql import GraphQLError
from assets.models import File, Image


def get_image(id: str|int) -> Image:
    """
    Gets and retuns an image with the specified `id`
    and thows a graphql error if the image was not found
    """
    try:
        return Image.objects.get(pk=id)
    except Image.DoesNotExist:
        raise GraphQLError(f"Image reccord with id {id} was not found")


def get_file(id: str|int) -> File:
    """
    Gets and retuns a file with the specified `id`
    and thows a graphql error if the file was not found
    """
    try:
        return File.objects.get(pk=id)
    except File.DoesNotExist:
        raise GraphQLError(f"File reccord with id {id} was not found")


class CloudinaryType:
    url: str
    public_id: str
