import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import Post
from . import services

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        text = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        post = services.createPost(kwargs, info)
        return CreatePost(post=post)

class PostQuery(graphene.ObjectType):
    posts = graphene.List(PostType)

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

class PostMutation(graphene.ObjectType):
    create_post = CreatePost.Field()
