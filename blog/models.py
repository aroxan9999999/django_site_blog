import os.path
from random import randint

from django.db import models


class Post(models.Model):
    author = models.ForeignKey("auth.USER", on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ImageField(upload_to="img/")
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Title")
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    like = models.BigIntegerField(default=0)
    published = models.BooleanField(default=False)


    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey("auth.USER", on_delete=models.CASCADE)
    text = models.TextField()
    time = models.CharField(max_length=15, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.post.title

class Like(models.Model):
    _like = models.ForeignKey("auth.USER", on_delete=models.CASCADE, blank=True, null=True, related_name='_like')
    _dislike = models.ForeignKey("auth.USER", on_delete=models.CASCADE, blank=True, null=True, related_name="_dislike")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="пост")


#class Dislike(models.Model):
#    _dislike = models.ForeignKey("auth.USER", on_delete=models.PROTECT, blank=True, null=True, related_name="_dislike")
#    post = models.ForeignKey(Post, on_delete=models.PROTECT, blank=True, null=True, related_name="_post")
#
