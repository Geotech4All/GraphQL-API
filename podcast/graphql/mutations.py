import graphene
from graphene_django.types import ErrorType
from graphene_file_upload.scalars import Upload
from graphql_auth.decorators import login_required
from .types import OrganizationType, AddressNode, GuestType
from .utils import perform_address_create, perform_address_update, perform_guest_create, perform_guest_update, perform_organization_create, perform_organization_update


class AddressCreateUpdateMutation(graphene.Mutation):
    """
    Performs create and update activity on an `Address`.
    To perform an update all you need to do is pass in the address `id`.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    address = graphene.Field(AddressNode)

    class Arguments:
        address_id = graphene.ID(description="The `id` of the address to be updated")
        city = graphene.String(required=True)
        state = graphene.String(required=True)
        country = graphene.String(required=True)
        address = graphene.String(required=True)
        zip_code = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        address_id = kwargs.get('address_id')
        if address_id:
            address = perform_address_update(info=info, **kwargs)
            return AddressCreateUpdateMutation(success=True, address=address)
        address = perform_address_create(info, **kwargs)
        return AddressCreateUpdateMutation(success=True, address=address)


class OrganizationCreateUpdateMutation(graphene.Mutation):
    """
    Performs create and update activiies on an `Organization`.
    To perform an update all you need to do is pass the organization `id`.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    organization = graphene.Field(OrganizationType)

    class Arguments:
        organization_id = graphene.ID(description="The `id` of the organization to be updated")
        name = graphene.String(required=True)
        address_id = graphene.ID()
        description = graphene.String()
        logo = Upload()
        email = graphene.String()
        phone = graphene.String()


    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        organization_id = kwargs.get('organization_id')
        if organization_id:
            organization = perform_organization_update(info, **kwargs)
            return OrganizationCreateUpdateMutation(success=True, organization=organization)
        organization = perform_organization_create(info, **kwargs)
        return OrganizationCreateUpdateMutation(success=True, organization=organization)


class GuestCreateUpdateMutation(graphene.Mutation):
    """
    Performs create and update actions on a `Guest` object.
    To perform an update all you need to do is pass in the guest `id`.
    """
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)
    guest = graphene.Field(GuestType)

    class Arguments:
        guest_id = graphene.ID(
            description="Pass this if you want to perform an update on a guest")
        name = graphene.String(required=True)
        description = graphene.String()
        organization_id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info: graphene.ResolveInfo, **kwargs):
        guest_id = kwargs.get('guest_id')
        if guest_id:
            guest = perform_guest_update(info, **kwargs)
            return GuestCreateUpdateMutation(success=True, guest=guest)
        guest = perform_guest_create(info, **kwargs)
        return GuestCreateUpdateMutation(success=True, gurst=guest)


class PodcastMutations(graphene.ObjectType):
    create_update_address = AddressCreateUpdateMutation.Field()
    create_update_organization = OrganizationCreateUpdateMutation.Field()
    create_update_guest = GuestCreateUpdateMutation.Field()
