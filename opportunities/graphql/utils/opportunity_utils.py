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
            abstract=kwargs.get("abstract"),
            content=kwargs.get("content"),
            category=Tag.objects.filter(title__iexact=kwargs.get("category_id")).first()
        )
    opportunity.save()
    return opportunity


def perform_opportunity_update(info: graphene.ResolveInfo, **kwargs) -> Opportunity:
    staff = validate_and_return_staff(info)
    if not (staff.can_update_opportunities or staff.user.is_superuser):
        raise GraphQLError("You are not permitted to create opportunites")

    opportunity_id = kwargs.get("opportunity_id")
    title = kwargs.get("title", None)
    abstract = kwargs.get("abstract")
    content  = kwargs.get("content")
    category_id = kwargs.get("category_id")

    opportunity = get_opportunity_by_id(str(opportunity_id))

    if title: opportunity.title = title
    if abstract: opportunity.abstract = abstract
    if content: opportunity.content = content
    if category_id: opportunity.category = Tag.objects.filter(title__iexact=category_id).first()
    opportunity.save()
    return opportunity
