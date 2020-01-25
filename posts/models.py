from django.db import models
from django.conf import settings

class Post(models.Model):
    imgurl = models.URLField(null=True)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
