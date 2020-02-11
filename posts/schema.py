import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import Post, Clap, Response
from . import services

# Types

class ResponseType(DjangoObjectType):
    class Meta:
        model = Response

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class ClapType(DjangoObjectType):
    class Meta:
        model = Clap

# Mutations

class DeletePost(graphene.Mutation):
    deleted = graphene.Boolean()

    class Arguments:
        post_id = graphene.Int()

    @login_required
    def mutate(self, info, post_id):
        is_deleted = services.deletePost(post_id, info)
        return DeletePost(deleted=is_deleted)

class DeleteResponse(graphene.Mutation):
    deleted = graphene.Boolean()

    class Arguments:
        response_id = graphene.Int()

    @login_required
    def mutate(self, info, response_id):
        is_deleted = services.deleteResponse(response_id, info)
        return DeleteResponse(deleted=is_deleted)

class CreateResponse(graphene.Mutation):
    response = graphene.Field(ResponseType)

    class Arguments:
        post_id = graphene.Int()
        text = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        response = services.createResponse(kwargs, info)
        return CreateResponse(response=response)

class ClapPost(graphene.Mutation):
    clap = graphene.Field(ClapType)

    class Arguments:
        post_id = graphene.Int()

    @login_required
    def mutate(self, info, post_id):
        clap = services.clapPost(post_id, info)
        return ClapPost(clap=clap)

class RemoveClap(graphene.Mutation):
    deleted = graphene.Boolean()

    class Arguments:
        post_id = graphene.Int()

    @login_required
    def mutate(self, info, post_id):
        is_deleted = services.removeClap(post_id, info)
        return RemoveClap(deleted=is_deleted)

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

class PostMutation(graphene.ObjectType):
    delete_post = DeletePost.Field()
    delete_response = DeleteResponse.Field()
    create_post = CreatePost.Field()
    create_response = CreateResponse.Field()
    update_post = UpdatePost.Field()
    clap_post = ClapPost.Field()
    remove_clap = RemoveClap.Field()

# Queries

class PostQuery(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, post_id=graphene.Int())
    response = graphene.Field(ResponseType, response_id=graphene.Int())

    def resolve_response(self, info, response_id):
        return services.response_by_id(response_id)

    def resolve_post(self, info, post_id):
        return services.post_by_id(post_id)

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()
