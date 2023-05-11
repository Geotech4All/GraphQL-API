from django.contrib.auth import get_user_model
import graphene
from graphql import GraphQLError
from core.utils import get_object_or_errror
from users.models import Staff


User = get_user_model()

def validate_and_return_staff(info: graphene.ResolveInfo) -> Staff:
    """
    Ensures the current user is a staff and returs that staff
    """
    try:
        return Staff.objects.get(user=info.context.user)
    except Staff.DoesNotExist:
        if info.context.user.is_superuser:
            staff = Staff.create_super_staff(info.context.user)
            return staff
        raise GraphQLError("You do not have staff authorization and are not authorized to perfom this action")


def perform_staff_update(info: graphene.ResolveInfo, **kwargs):
    """
    Performs update on staff permisions
    """
    if not info: raise ValueError("info is required")

    staff_user = validate_and_return_staff(info)
    if not (staff_user.can_create_user or staff_user.can_alter_user or staff_user.user.is_superuser):
        raise GraphQLError("You are not authorized to update staff permissions")

    user_email = kwargs.get("user_email")
    if not user_email: raise GraphQLError("staff_id is required to perform an update")

    staff = get_object_or_errror(Staff, user__email=user_email)
    if kwargs.get("can_create_post", None): staff.can_create_post = kwargs.get("can_create_post")
    if kwargs.get("can_alter_post", None): staff.can_alter_post = kwargs.get("can_alter_post")
    if kwargs.get("can_delete_post", None): staff.can_delete_post = kwargs.get("can_delete_post")
    if kwargs.get("can_create_user", None): staff.can_create_user = kwargs.get("can_create_user")
    if kwargs.get("can_alter_user", None): staff.can_alter_user = kwargs.get("can_alter_user")
    if kwargs.get("can_delete_user", None): staff.can_delete_user = kwargs.get("can_delete_user")
    if kwargs.get("can_create_podcast", None): staff.can_create_podcast = kwargs.get("can_create_podcast")
    if kwargs.get("can_alter_podcast", None): staff.can_alter_podcast = kwargs.get("can_alter_podcast")
    if kwargs.get("can_delete_podcast", None): staff.can_delete_podcast = kwargs.get("can_delete_podcast")
    if kwargs.get("can_create_opportunities", None): staff.can_create_opportunities = kwargs.get("can_create_opportunities")
    if kwargs.get("can_update_opportunities", None): staff.can_update_opportunities = kwargs.get("can_update_opportunities")
    if kwargs.get("can_delete_opportunities", None): staff.can_delete_opportunities = kwargs.get("can_delete_opportunities")
    staff.save() #type: ignore
    return staff


def perform_staff_create(info: graphene.ResolveInfo, **kwargs) -> Staff:
    staff_user = validate_and_return_staff(info)

    if not (staff_user.can_create_user or staff_user.can_alter_user or staff_user.user.is_superuser):
        raise GraphQLError("You are not authorized to perform staff promotion")

    user_email = kwargs.get("user_email")
    if not user_email: raise GraphQLError("user_email is required")
    
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        raise GraphQLError('A user with the specified email does not exist')

    if Staff.objects.filter(user=user).count():
        raise GraphQLError("This user already has staff privilledges")
    else:
        staff: Staff = Staff.objects.create(user=user)
        if kwargs.get("can_create_post", None): staff.can_create_post = kwargs.get("can_create_post")
        if kwargs.get("can_alter_post", None): staff.can_alter_post = kwargs.get("can_alter_post")
        if kwargs.get("can_delete_post", None): staff.can_delete_post = kwargs.get("can_delete_post")
        if kwargs.get("can_create_user", None): staff.can_create_user = kwargs.get("can_create_user")
        if kwargs.get("can_alter_user", None): staff.can_alter_user = kwargs.get("can_alter_user")
        if kwargs.get("can_delete_user", None): staff.can_delete_user = kwargs.get("can_delete_user")
        if kwargs.get("can_create_podcast", None): staff.can_create_podcast = kwargs.get("can_create_podcast")
        if kwargs.get("can_alter_podcast", None): staff.can_alter_podcast = kwargs.get("can_alter_podcast")
        if kwargs.get("can_delete_podcast", None): staff.can_delete_podcast = kwargs.get("can_delete_podcast")
        if kwargs.get("can_create_opportunities", None): staff.can_create_opportunities = kwargs.get("can_create_opportunities")
        if kwargs.get("can_update_opportunities", None): staff.can_update_opportunities = kwargs.get("can_update_opportunities")
        if kwargs.get("can_delete_opportunities", None): staff.can_delete_opportunities = kwargs.get("can_delete_opportunities")
        staff.save()
        return staff
