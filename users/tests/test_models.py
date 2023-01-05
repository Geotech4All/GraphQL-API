from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import CustomUser, Profile

class CustomUserAndProfileModelTests(TestCase):
    """
    Contains all tests for the CustomUser and Profile models
    """

    def test_profile_is_created_after_user_is_created(self):
        test_user = CustomUser.objects.create_user(email="example@email.com", password="password")
        profile = Profile.objects.filter(user=test_user)[0]
        self.assertIsNotNone(profile)
