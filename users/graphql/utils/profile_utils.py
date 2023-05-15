import graphene
from django.shortcuts import get_object_or_404
from graphql import GraphQLError
from assets.utils import get_image
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
    first_name = kwargs.get("first_name", None)
    last_name = kwargs.get("last_name", None)
    about = kwargs.get("about", None)
    image_id = kwargs.get("image_id", None)

    if first_name is not None: user.first_name = first_name
    if last_name is not None: user.last_name = last_name

    if about is not None: profile.about = about
    if image_id is not None: profile.image = get_image(str(image_id))

    user.save() #type: ignore
    profile.save()
    return profile
