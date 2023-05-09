import graphene
from django.shortcuts import get_object_or_404
from graphql import GraphQLError
from users.models import CustomUser, Profile
from core.utils import get_object_or_errror


def perform_profile_update(info:graphene.ResolveInfo, **kwargs: str) -> Profile:
    """
    Performs update on a profile and returns the updated profile
    """
    profile_id = kwargs.get("profile_id", None)
    assert profile_id, GraphQLError("Profile `id` is required")
    profile = get_object_or_404(Profile, pk=profile_id)
    assert (info.context.user == profile.user), GraphQLError("You are not authorised to perform this action")
    user = get_object_or_errror(CustomUser, pk=profile.user.pk)
    user.first_name = kwargs.get("first_name", user.first_name)
    user.last_name = kwargs.get("last_name", user.last_name)
    user.save() #type:ignore
    profile.image = kwargs.get("image", profile.image)
    profile.about = kwargs.get("about", profile.about)
    profile.save()
    return profile
