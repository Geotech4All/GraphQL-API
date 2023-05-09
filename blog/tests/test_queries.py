from django.test import TestCase
import graphene
from .constants.queries import popular_posts_query

from core.schema import Query


class BlogPostQueriesTestCase(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.query = popular_posts_query
        super().__init__(methodName)

    def setUp(self) -> None:
        self.schema = graphene.Schema(query=Query)
        return super().setUp()
        
    def test_get_popular_posts(self):
        response = self.schema.execute(self.query)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.errors)

