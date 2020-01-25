import graphene
import graphql_jwt

from users.schema import UserQuery, UserMutation, UserType
from posts.schema import PostMutation, PostQuery

class RootQuery(UserQuery, PostQuery, graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not log in!')
        return user

class RootMutation(UserMutation, PostMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
