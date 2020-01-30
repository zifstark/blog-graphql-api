from django.contrib.auth import get_user_model
from .models import Post

def createPost(input, info):
    c_user = info.context.user
    new_post = Post(title=input['title'], text=input['text'], author=c_user)
    print(new_post.author)
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
