import graphene
from graphene_django import DjangoObjectType
from users.models import Staff, CustomUser

 
class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "full_name", "first_name", "last_name", "email")

class StaffType(DjangoObjectType):
    user = graphene.Field(UserType)
    staff_id = graphene.ID()
    class Meta:
        model = Staff
        fields = ('id', 'user', 'can_create_post')
        interfaces = (graphene.relay.Node, )


    def resolve_user(self, _):
        if isinstance(self, Staff):
            return self.user
        return None

    def resolve_staff_id(self, _):
        if isinstance(self, Staff):
            return self.pk
        return None
