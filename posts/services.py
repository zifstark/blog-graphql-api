from django.contrib.auth import get_user_model
from .models import Post, Clap

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
    return clap
