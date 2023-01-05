from django.test import TestCase
from podcast.models import Guest, Podcast

from users.models import CustomUser

class TestPodcastAndGuestModels(TestCase):
    """
    Contains all tests for Podcast and Guest models
    """
    def test_podcast_create_with_guests_and_hosts(self):
        test_user1 = CustomUser.objects.create_user(email="test@dev.com", password="testing101")
        test_user2 = CustomUser.objects.create_user(email="test2@dev.com", password="testing101")
        test_guest1 = Guest.objects.create(name="tester1", description="loves testing everyday")
        test_guest2 = Guest.objects.create(name="tester2", description="loves testing everyday")
        test_posdcast:Podcast = Podcast.objects.create(
            title="Test podcast",
            description="ensuring podcast creation works")
        test_posdcast.hosts.add(test_user1)
        test_posdcast.hosts.add(test_user2)
        test_posdcast.guests.add(test_guest1)
        test_posdcast.guests.add(test_guest2)
        test_posdcast.save()
        self.assertIsNotNone(test_posdcast.hosts.all()[1])
        self.assertTrue(len(test_posdcast.guests.all()) == 2)
