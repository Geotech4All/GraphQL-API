import graphene
from graphene_django import DjangoObjectType
from podcast.models import Host
from users.models import Profile, Staff, CustomUser


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        exclude = ("password", "last_login", "is_staff", "is_active", "is_superuser", "date_joined", "username")


class StaffType(DjangoObjectType):
    user = graphene.Field(UserType)
    staff_id = graphene.ID()
    class Meta:
        model = Staff
        fields = (
            'id', 'user',
            'can_create_post',
            'can_alter_post',
            'can_delete_post',
            'can_create_user',
            'can_alter_user',
            'can_delete_user',
            'can_create_podcast',
            'can_alter_podcast',
            'can_delete_podcast')
        interfaces = (graphene.relay.Node, )


    def resolve_user(self, _):
        if isinstance(self, Staff):
            return self.user
        return None

    def resolve_staff_id(self, _):
        if isinstance(self, Staff):
            return self.pk
        return None

class ProfileType(DjangoObjectType):
    user = graphene.Field(UserType)
    image = graphene.String()
    profile_id = graphene.ID()
    class Meta:
        model = Profile
        fields = ("user", "about")

    def resolve_user(self, _):
        if isinstance(self, Profile):
            return self.user
        return None

    def resolve_image(self, _):
        if isinstance(self, Profile):
            return self.get_image_url
        return None

    def resolve_profile_id(self, _):
        if isinstance(self, Profile):
            return self.pk
        return None
