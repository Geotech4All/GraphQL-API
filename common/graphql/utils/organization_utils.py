import graphene
from graphql import GraphQLError
from assets.utils import get_image

from common.models import Organization
from common.utils import get_organization
from users.graphql.utils.staff_utils import validate_and_return_staff


def perform_organization_update(info: graphene.ResolveInfo, **kwargs) -> Organization:
    validate_and_return_staff(info)
    organization_id = kwargs.get("organization_id")
    assert organization_id, GraphQLError("organization_id is required for update")

    organization = get_organization(organization_id)

    name = kwargs.get("name")
    description = kwargs.get("description")
    logo_id = kwargs.get("logo_id")

    if name: organization.name = name
    if description: organization.description = description
    if logo_id: organization.logo = get_image(logo_id)

    organization.save()
    return organization


def perform_organization_create(info: graphene.ResolveInfo, **kwargs) -> Organization:
    validate_and_return_staff(info)
    return Organization(
        name = kwargs.get("name"),
        description = kwargs.get("description"),
        logo_id = get_image(str(kwargs.get("logo_id"))) if kwargs.get("logo_id") else None
    )
