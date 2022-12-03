from graphene_django import DjangoObjectType
from users.models import Staff


class StaffType(DjangoObjectType):
    class Meta:
        model = Staff
        fields = ('id', 'user', 'can_create_post')
