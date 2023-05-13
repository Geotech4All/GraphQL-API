import graphene
from graphql import GraphQLError
from assets.models import File
from assets.utils import get_file

from users.graphql.utils.staff_utils import validate_and_return_staff


def perform_file_update(info: graphene.ResolveInfo, **kwargs):
    validate_and_return_staff(info)
    file_id = kwargs.get("file_id", None)
    assert file_id is not None, GraphQLError("file_id is required for an update")

    file = get_file(str(file_id))
    return file.update(
            file=kwargs.get("file", None),
            name=kwargs.get("name", None),
            description=kwargs.get("description", None)
        )


def perform_file_create(info: graphene.ResolveInfo, **kwargs):
    validate_and_return_staff(info)
    file = kwargs.get("file", None)
    name = kwargs.get("name", None)
    assert file is not None, GraphQLError("file is required for File create")
    assert name is not None, GraphQLError("name is required for File create")
    return File.new(
            file=file, name=name,
            description=kwargs.get("description"),
            folder=kwargs.get("folder")
        )


def perform_file_delete(info: graphene.ResolveInfo, **kwargs):
    validate_and_return_staff(info)
    file_id = kwargs.get("file_id")
    assert file_id is not None, GraphQLError("file_id is required for an update")
    file = get_file(id=str(file_id))
    file.delete()
    return True
