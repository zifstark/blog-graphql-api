import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import Post, Clap
from . import services

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class ClapType(DjangoObjectType):
    class Meta:
        model = Clap

class ClapPost(graphene.Mutation):
    clap = graphene.Field(ClapType)

    class Arguments:
        post_id = graphene.Int()

    @login_required
    def mutate(self, info, post_id):
        clap = services.clapPost(post_id, info)
        return ClapPost(clap=clap)

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String()
        text = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        post = services.createPost(kwargs, info)
        return CreatePost(post=post)

class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        postId = graphene.String(required=True)
        text = graphene.String()
        title = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        post = services.updatePost(kwargs, info)
        return UpdatePost(post=post)

class PostQuery(graphene.ObjectType):
    posts = graphene.List(PostType)

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

class PostMutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    clap_post = ClapPost.Field()
