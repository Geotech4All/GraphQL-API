import graphene
from graphene_django.types import ErrorType
from graphql_auth import mutations
from graphql_auth.decorators import login_required
from users.graphql.utils.staff_utils import perform_staff_create, perform_staff_update
from users.graphql.utils.user_utils import handle_create_superuser
from .types import ProfileType, StaffType, UserType
from .utils.profile_utils import perform_profile_update


class SuperUserCreateMutation(graphene.Mutation):
    """
    Classified
    """
    success = graphene.Boolean()
    user = graphene.Field(UserType)
    errors = graphene.List(ErrorType)

    class Arguments:
        email = graphene.String(required=True, description="User email")
        password1 = graphene.String(required=True, description="User password")
        password2 = graphene.String(required=True, description="Confirm password")
        secret_code = graphene.String()

    @classmethod
    def mutate(cls, root, _: graphene.ResolveInfo, **kwargs):
        user = handle_create_superuser(**kwargs)
        return SuperUserCreateMutation(user=user, success=True)


class StaffCreateMutation(graphene.Mutation):
    """
    Promote existing user to staff with certan permisions
    """
    staff = graphene.Field(StaffType)
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)

    class Arguments:
        user_email = graphene.String(
            required=True,
            description="The email of the user to be promoted to staff")
        can_create_post = graphene.Boolean()
        can_alter_post = graphene.Boolean()
        can_delete_post = graphene.Boolean()
        can_create_user = graphene.Boolean() 
        can_alter_user = graphene.Boolean()
        can_delete_user = graphene.Boolean() 
        can_create_podcast = graphene.Boolean()
        can_alter_podcast = graphene.Boolean() 
        can_delete_podcast = graphene.Boolean()
        can_create_opportunities = graphene.Boolean()
        can_update_opportunities = graphene.Boolean()
        can_delete_opportunities = graphene.Boolean()


    @classmethod
    @login_required
    def mutate(cls, _, info: graphene.ResolveInfo, **kwargs):
        new_staff = perform_staff_create(info, **kwargs)
        return StaffCreateMutation(staff=new_staff, success=True)


class StaffUpdateMutation(graphene.Mutation):
    """
    Perfoms update operations on a staff
    Mostly staff permisions
    """
    staff = graphene.Field(StaffType)
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)

    class Arguments:
        user_email = graphene.String(
            required=True,
            description="The email of the user to be promoted to staff")
        can_create_post = graphene.Boolean()
        can_alter_post = graphene.Boolean()
        can_delete_post = graphene.Boolean()
        can_create_user = graphene.Boolean() 
        can_alter_user = graphene.Boolean()
        can_delete_user = graphene.Boolean() 
        can_create_podcast = graphene.Boolean()
        can_alter_podcast = graphene.Boolean() 
        can_delete_podcast = graphene.Boolean()
        can_create_opportunities = graphene.Boolean()
        can_update_opportunities = graphene.Boolean()
        can_delete_opportunities = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, _, info: graphene.ResolveInfo, **kwargs):
        updated_staff = perform_staff_update(info, **kwargs)
        return StaffUpdateMutation(staff=updated_staff, success=True)


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
        image_id = graphene.ID()
        about = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, _, info:graphene.ResolveInfo, **kwargs):
        profile = perform_profile_update(info, **kwargs)
        return ProfileUpdateMutation(profile=profile, success=True)

class AuthMutations(graphene.ObjectType):
    create_super_user = SuperUserCreateMutation.Field()

    update_profile = ProfileUpdateMutation.Field()
    create_staff = StaffCreateMutation.Field()
    update_staff = StaffUpdateMutation.Field()
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

