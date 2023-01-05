import graphene #type: ignore
from graphene_django.types import ErrorType
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError #type: ignore
from graphql_auth import mutations #type: ignore
from graphql_auth.decorators import login_required
from graphql_auth.mixins import get_user_model #type: ignore
from users.models import Staff, CustomUser
from .types import ProfileType, StaffType
from .utils import perform_profile_update

User = get_user_model()

class StaffCreateUpdateMutation(graphene.Mutation):
    staff = graphene.Field(StaffType)
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)

    class Arguments:
        user_email = graphene.String(
            required=True,
            description="The email of the user to be promoted to staff")
        can_create_post = graphene.Boolean()


    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        admin: CustomUser = info.context.user
        if admin.is_staff:
            try:
                user = User.objects.get(email=kwargs.get('user_email'))
                staff: Staff = Staff.objects.create(user=user, can_create_post=kwargs.get('can_create_post'))
                staff.save()
                return StaffCreateUpdateMutation(staff=staff, success=True)
            except User.DoesNotExist:
                raise GraphQLError('A user with the specified email does not exist')
        else:
            raise GraphQLError("You do not have permissions to alter the user")

class ProfileUpdateMutation(graphene.Mutation):
    """
    Prefroms all update operations of a users Profile
    """
    profile = graphene.Field(ProfileType)
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)

    class Arguments:
        profile_id = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        image = Upload()
        about = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, _, info:graphene.ResolveInfo, **kwargs):
        profile = perform_profile_update(info, **kwargs)
        return ProfileUpdateMutation(profile=profile, success=True)

class AuthMutations(graphene.ObjectType):
    update_profile = ProfileUpdateMutation.Field()
    create_update_staff = StaffCreateUpdateMutation.Field()
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
