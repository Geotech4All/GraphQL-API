import graphene
from graphql import GraphQLError
from assets.models import Tag
from common.utils import get_location, get_organization
from opportunities.models import Opportunity

from users.graphql.utils.staff_utils import validate_and_return_staff

def get_opportunity_by_id(id: str) -> Opportunity:
    try:
        opp: Opportunity = Opportunity.objects.get(id=id)
        return opp
    except Opportunity.DoesNotExist:
       raise GraphQLError("The specified opportunity was not found")


def perform_opportunity_create(info: graphene.ResolveInfo, **kwargs)-> Opportunity:
    staff = validate_and_return_staff(info)
    if not (staff.can_create_opportunities or staff.user.is_superuser):
        raise GraphQLError("You are not permitted to create opportunites")

    title = kwargs.get("title")
    tag_ids = kwargs.get("tag_ids")
    organization_id = kwargs.get("organization_id")
    location_id = kwargs.get("location_id")

    if not title: raise GraphQLError("Title is required")
    opportunity: Opportunity = Opportunity.objects.create(
            title=title,
            content=kwargs.get("content"),
            description = kwargs.get("description"),
        )

    if tag_ids: opportunity.tags = Tag.objects.filter(pk__in=tag_ids)
    if organization_id: opportunity.organization = get_organization(organization_id)
    if location_id: opportunity.location = get_location(location_id)

    opportunity.save()
    return opportunity


def perform_opportunity_update(info: graphene.ResolveInfo, **kwargs) -> Opportunity:
    staff = validate_and_return_staff(info)
    if not (staff.can_update_opportunities or staff.user.is_superuser):
        raise GraphQLError("You are not permitted to create opportunites")

    opportunity_id = kwargs.get("opportunity_id")
    assert opportunity_id, GraphQLError("opportunity_id is required for update")
    title = kwargs.get("title", None)
    content  = kwargs.get("content", None)

    #Update
    description = kwargs.get("description")
    tag_ids = kwargs.get("tag_ids")
    organization_id = kwargs.get("organization_id")
    location_id = kwargs.get("location_id")

    opportunity = get_opportunity_by_id(str(opportunity_id))

    if title: opportunity.title = title
    if content: opportunity.content = content

    # Updates
    if description: opportunity.description = description
    if tag_ids: opportunity.tags = Tag.objects.filter(tags__id__in=tag_ids)
    if organization_id: opportunity.organization = get_organization(organization_id)
    if location_id: opportunity.location = get_location(location_id)
    opportunity.save()
    return opportunity
