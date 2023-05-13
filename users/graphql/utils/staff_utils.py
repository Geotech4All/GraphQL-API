from typing import cast
from django.contrib.auth import get_user_model
import graphene
from graphql import GraphQLError
from core.utils import get_object_or_errror
from users.models import CustomUser, Staff


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

staff_fields = [
        "can_create_post", "can_alter_post", "can_delete_post",
        "can_create_user", "can_alter_user", "can_delete_user",
        "can_create_podcast", "can_alter_podcast", "can_delete_podcast", 
        "can_create_opportunities", "can_update_opportunities", "can_delete_opportunities"
    ]

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
    user = cast(CustomUser, get_object_or_errror(User, email=user_email))
    staff = get_object_or_errror(Staff, user__email=user_email)
    for field in staff_fields:
        field_value = kwargs.get(field)
        if hasattr(Staff, field): setattr(staff, field, field_value)
    user.is_staff = True
    user.save()
    staff.save() #type: ignore
    print(staff.can_update_opportunities)
    return staff


def perform_staff_create(info: graphene.ResolveInfo, **kwargs) -> Staff:
    staff_user = validate_and_return_staff(info)

    if not (staff_user.can_create_user or staff_user.can_alter_user or staff_user.user.is_superuser):
        raise GraphQLError("You are not authorized to perform staff promotion")

    user_email = kwargs.get("user_email")
    if not user_email: raise GraphQLError("user_email is required")

    user = cast(CustomUser, get_object_or_errror(User, email=user_email))

    if Staff.objects.filter(user=user).count():
        raise GraphQLError("This user already has staff privilledges")
    else:
        staff: Staff = Staff.objects.create(user=user)
        for field in staff_fields:
            field_value = kwargs.get(field)
            if hasattr(Staff, field): setattr(staff, field, field_value)
        user.is_staff = True
        user.save()
        staff.save()
        return staff
