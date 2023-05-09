from django.test import TestCase
import graphene

from core.schema import Mutation, Query
from .constants.mutations import create_update_post_image


class PostImageMutationsTestCase(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.post_image_mutation = create_update_post_image
        super().__init__(methodName)

    def setUp(self) -> None:
        print("Setting up PostImageMutationsTestCase")
        self.schema = graphene.Schema(query=Query, mutation=Mutation)
        return super().setUp()

    def test_can_create_post_image(self):
        print("running test_can_create_post_image")
        response = self.schema.execute(self.post_image_mutation)
        print(response)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.errors)
