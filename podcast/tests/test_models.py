from django.test import TestCase
from podcast.models import Guest, Podcast

class PodcastTestCase(TestCase):
    """
    Contains all tests for Podcast and Guest models
    """
    def _get_created_podcast(self) -> Podcast:
        return Podcast.objects.get(title="Test podcast")

    def setUp(self) -> None:
        Podcast.objects.create(title="Test podcast", description="enduring podcast creation works")

    def test_podcast_was_created(self):
        podcast = self._get_created_podcast()
        self.assertIsNotNone(podcast)

    def test_can_add_guest_to_podcast(self):
        guest = Guest.objects.create(name="Test guest", description="guest for test")
        podcast = self._get_created_podcast()
        podcast.guests.add(guest)
        podcast.save()
        first_guest = podcast.guests.all()[0]
        self.assertIsNotNone(first_guest)
        self.assertTrue(first_guest.name=="Test guest")

