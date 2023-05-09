import graphene
from graphql import GraphQLError
from users.graphql.utils.staff_utils import validate_and_return_staff
from assets.models import Tag


def perform_tag_create(info: graphene.ResolveInfo, **kwargs) -> Tag:
    validate_and_return_staff(info)
    tag: Tag = Tag.objects.create(
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            category=kwargs.get("category"))
    return tag


def perform_tag_update(info: graphene.ResolveInfo, **kwargs) -> Tag:
    validate_and_return_staff(info)
    tag_id = kwargs.get("tag_id")
    if not tag_id:
        raise GraphQLError("tag_id is required")
    try:
        tag: Tag = Tag.objects.get(id=tag_id)
        if kwargs.get("category"): tag.category = kwargs.get("category")
        if kwargs.get("title"): tag.title = kwargs.get("title")
        if kwargs.get("description"): tag.description = kwargs.get("description")
        tag.save()
        return tag
    except Tag.DoesNotExist:
        raise GraphQLError("The specified tag was not found")
