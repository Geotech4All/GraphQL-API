from typing import cast
from graphql import GraphQLError
from core.settings import SUPER_USER_CODE
from django.contrib.auth import get_user_model

from users.models import CustomUser, Staff

User = cast(CustomUser, get_user_model())

def handle_create_superuser(**kwargs) -> CustomUser:
    email = str(kwargs.get("email"))
    password1 = str(kwargs.get("password1"))
    password2 = str(kwargs.get("password2"))
    secret_code = kwargs.get("secret_code", None)
    if not password1 == password2:
        raise GraphQLError("Passwords do not match")
    if not secret_code or str(secret_code) != SUPER_USER_CODE:
        raise GraphQLError("Missing or invalid CODE! You are not authorized to perform this action")
    user = User.objects.create_superuser(email=email, password=password1)
    Staff.create_super_staff(user)
    return cast(CustomUser, user)
