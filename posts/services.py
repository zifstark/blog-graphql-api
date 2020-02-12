from django.contrib.auth import get_user_model
from .models import Post, Clap, Response

def updateResponse(input, info):
    response = Response.objects.filter(id=input.get('response_id', 0)).first()
    if not response:
        raise Exception('Response not found!')
    c_user = info.context.user
    if c_user.id != response.author.id:
        raise Exception('Unauthorize action!')
    response.text = input.get('text', response.text)
    response.save()
    return response

def deletePost(post_id, info):
    post = Post.objects.filter(id=post_id).first()
    if not post:
        return False
    c_user = info.context.user
    if c_user.id != post.author.id:
        raise Exception('Unauthorize action!')
    post.delete()
    return True

def deleteResponse(response_id, info):
    response = Response.objects.filter(id=response_id).first()
    if not response:
        return False
    c_user = info.context.user
    if c_user.id != response.author.id:
        raise Exception('Unauthorize action!')
    results = response.delete()
    return True

def response_by_id(response_id):
    response = Response.objects.filter(id=response_id).first()
    if not response:
        raise Exception('Response not found!')
    return response

def post_by_id(post_id):
    post = Post.objects.filter(id=post_id).first()
    if not post:
        raise Exception('Post not found!')
    return post

def createResponse(input, info):
    post = Post.objects.filter(id=input['post_id']).first()
    if not post:
        raise Exception('Post not found')
    c_user = info.context.user
    new_response = Response(
        post=post,
        author=c_user,
        text=input.get('text', '')
    )
    new_response.save()
    return new_response


def removeClap(post_id, info):
    post = Post.objects.filter(id=post_id).first()
    if not post:
        raise Exception('Post not found')
    c_user = info.context.user
    results = Clap.objects.filter(post=post, user=c_user).delete()
    post.claps_count -= 1
    post.save()
    return results[0] > 0

def createPost(input, info):
    c_user = info.context.user
    new_post = Post(title=input['title'], text=input['text'], author=c_user)
    new_post.save()
    return new_post

def updatePost(input, info):
    c_user = info.context.user
    post = Post.objects.get(pk=int(input['postId']))
    if c_user.id != post.author.id:
        raise Exception('Unauthorize action!')
    post.title = input.get('title', post.title)
    post.text = input.get('text', post.text)
    post.save()
    return post

def clapPost(post_id, info):
    post = Post.objects.filter(id=post_id).first()
    c_user = info.context.user
    clap = Clap.objects.filter(user=c_user, post=post).first()
    if clap:
        raise Exception('Cannot clap for a post more than once!')
    if not post:
        raise Exception('Post not found')
    new_clap = Clap(
        user=c_user,
        post=post
    )
    new_clap.save()
    post.claps_count += 1
    post.save()
    return clap
