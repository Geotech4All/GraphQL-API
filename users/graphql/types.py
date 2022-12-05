from graphene_django import DjangoObjectType
from users.models import Staff, CustomUser

 
class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name", "email", "username")

class StaffType(DjangoObjectType):
    class Meta:
        model = Staff
        fields = ('id', 'user', 'can_create_post')
