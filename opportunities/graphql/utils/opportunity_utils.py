import graphene
from graphql import GraphQLError
from assets.models import Image, Tag
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
    if not title: raise GraphQLError("Title is required")
    opportunity: Opportunity = Opportunity.objects.create(
            title=title,
            description=kwargs.get("description"),
            category=Tag.objects.filter(title__iexact=kwargs.get("category")).first()
        )
    image_ids = kwargs.get("image_ids")
    if image_ids:
        opportunity.images = Image.objects.filter(pk__in=list(image_ids))
    opportunity.save()
    return opportunity


def perform_opportunity_update(info: graphene.ResolveInfo, **kwargs) -> Opportunity:
    staff = validate_and_return_staff(info)
    if not (staff.can_update_opportunities or staff.user.is_superuser):
        raise GraphQLError("You are not permitted to create opportunites")

    opportunity_id = kwargs.get("opportunity_id")
    title = kwargs.get("title", None)
    description = kwargs.get("description")
    image_ids = kwargs.get("image_ids")
    category = kwargs.get("category")

    opportunity = get_opportunity_by_id(str(opportunity_id))

    if title: opportunity.title = title
    if description: opportunity.description = description
    if category: opportunity.category = Tag.objects.filter(title__iexact=category).first()
    if image_ids:
        opportunity.images = Image.objects.filter(pk__in=list(image_ids))
    opportunity.save()
    return opportunity
