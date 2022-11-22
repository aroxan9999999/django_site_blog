from django import forms
from .models import Post, Comment, Like


class Post_form(forms.ModelForm):
    class Meta:

        model = Post
        fields = ("category", "photo", "title", "text")

class Coment_Form(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)

class Like_form(forms.ModelForm):

    class Meta:
        model = Like
        fields = ("_like", "_dislike")