import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required, user_passes_test
from . import services

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class DeleteUser(graphene.Mutation):
    deleted = graphene.Boolean()

    class Arguments:
        userId = graphene.String(required=True)

    @login_required
    def mutate(self, info, userId):
        isDeleted = services.deleteUser(userId, info)
        return DeleteUser(deleted=isDeleted)

class SignUp(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(username=username, email=email)
        user.set_password(password)
        user.save()
        return SignUp(user=user)

class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        user = services.updateUser(kwargs, info)
        return UpdateUser(user=user)


class UserMutation(graphene.ObjectType):
    sign_up = SignUp.Field()
    delete_user = DeleteUser.Field()
    update_user = UpdateUser.Field()

class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()
