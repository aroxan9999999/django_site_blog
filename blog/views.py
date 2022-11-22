from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import Post_form, Coment_Form, Like_form
from .models import Post, Comment, Like, Category

__elem = {"element": None}
__view_post = {"view": True}


def _like(request, value):
    __like, _pk = value.split()
    _post = Post.objects.get(pk=_pk)
    if __like == "like":
        like = Like.objects.filter(_like=request.user, post__pk=_pk)
        if like:
            like[0]._like = None
            _post.like -= 1
            _post.save()
            like[0].save()
        else:
            like = Like.objects.filter(Q(_like=request.user) | Q(_dislike=request.user), post__pk=_pk)
            if like:
                like.delete()
            like_model = Like(_like=request.user, post=_post)
            _post.like += 1
            _post.save()
            like_model.save()
    else:
        dislike = Like.objects.filter(_dislike=request.user, post__pk=_pk)
        if dislike:
            dislike[0]._dislike = None
            dislike[0].save()
        else:
            dislike = Like.objects.filter(Q(_like=request.user) | Q(_dislike=request.user), post__pk=_pk)
            if dislike:
                dislike[0].delete()
                _post.like -= 1
                _post.save()
                print("dislike")
            dislike_model = Like(_dislike=request.user, post=Post.objects.get(pk=_pk))
            dislike_model.save()
    delete = Like.objects.filter(_like=None, _dislike=None).delete()


def __post_like(request):
    element = None
    if request.method == "POST":
        value1 = request.POST.get("like")
        value2 = request.POST.get("dislike")
        like = _like(request, value1) if value1 else _like(request, value2)
        pk = value1.split()[1] if value1 else value2.split()[1]
        element = pk
    else:
        if __elem["element"]:
            element = __elem["element"]
            __elem["element"] = None
    return element


def post_list(request):
    title = "главная страница"
    element = __post_like(request)
    __view_post["view"] = True
    _post = Post.objects.all().order_by("-publish_date")
    post = {}
    for key in _post:
        like = (key, Like.objects.filter(post=key).exclude(_like=None).count(),
                Like.objects.filter(post=key).exclude(_dislike=None).count())
        post[like] = Comment.objects.filter(post=key).order_by("-date")[:7]
    return render(request, "post_list.html", context={"post": post, "element": element})


def post_detail(request, post_pk):
    __post_like(request)
    detail = Post.objects.get(pk=post_pk)
    view = True if detail.author != request.user and __view_post["view"] else False
    comment = Comment.objects.filter(post=detail).order_by("-date")
    dislike = Like.objects.filter(post=detail).exclude(_dislike=None).count()
    __elem["element"] = post_pk
    return render(request, "post_detail.html", context={"post": detail, "comment": comment, "dislike": dislike, "view": view})


def new_post(request):
    form = Post_form(request.POST, request.FILES)
    operation = "создать"
    if form.is_valid():
        post = form.save(commit=False)
        post.publish_date = datetime.now()
        post.created_date = datetime.now()
        post.author = request.user
        post.photo = request.FILES["photo"]
        post.save()
        return redirect("post_detail", post_pk=post.pk)
    return render(request, "new_post.html", context={"form": form, "operation": operation})


def post_update(request, post_pk):
    operation = "обнавить"
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "GET":
        form = Post_form(instance=post)
        return render(request, "new_post.html", context={"form": form, "operation": operation})
    else:
        form = Post_form(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.publish_date = datetime.now()
            post.created_date = datetime.now()
            post.save()
            return redirect("post_detail", post_pk=post.pk)


def post_delete(request, post_pk):
    post = Post.objects.get(pk=post_pk).delete()
    return redirect("post_list")


def comment_post(request, post_pk):
    activated = True
    post = Post.objects.get(pk=post_pk)
    form = Coment_Form(request.POST or None)
    if form.is_valid():
        _time = datetime.now()
        time = f"{_time.hour}:{_time.minute}"
        _form = form.save(commit=False)
        _form.post = post
        _form.time = time
        _form.author = request.user
        _form.save()
        return redirect("post_detail", post_pk=post.pk)
    return render(request, "post_detail.html", context={"coment_form": form, "post": post, "activated": activated})


def my_post(request):
    element = __post_like(request)
    _post = Post.objects.filter(author=request.user).order_by("publish_date")
    post = {}
    for key in _post:
        like = (key, key.like,
                Like.objects.filter(post=key).exclude(_dislike=None).count())
        post[like] = Comment.objects.filter(post=key).order_by("-date")[:7]
    return render(request, "post_list.html", context={"post": post, "element": element})


def top_post(request):
    title = "top post"
    __view_post["view"] = True
    element = __post_like(request)
    _post = Post.objects.filter().order_by("-like")[:100]
    post = {}
    for key in _post:
        like = (key, key.like, Like.objects.filter(post=key).exclude(_dislike=None).count())
        post[like] = Comment.objects.filter(post=key).order_by("-date")[:7]
    return render(request, "post_list.html", context={"post": post, "element": element, "title": title})

def category(request):
    _category = []
    for i in Category.objects.all():
        _category.append((i.name, Post.objects.filter(category=i).first()))

    return render(request, "category.html", context={"category": _category})

def category_post(request, name):
    title = f"category {name}"
    element = __post_like(request)
    _post = Post.objects.filter(category__name=name).order_by("publish_date")
    post = {}
    for key in _post:
        like = (key, key.like, Like.objects.filter(post=key).exclude(_dislike=None).count())
        post[like] = Comment.objects.filter(post=key).order_by("-date")[:7]
    return render(request, "post_list.html", context={"post": post, "element": element, "title": title})


def user_post(request, user_name):
    __view_post["view"] = False
    title = user_name
    __elem["element"] = None
    element = __post_like(request)
    _post = Post.objects.filter(author__username=user_name).order_by("publish_date")
    post = {}
    for key in _post:
        like = (key, key.like, Like.objects.filter(post=key).exclude(_dislike=None).count())
        post[like] = Comment.objects.filter(post=key).order_by("-date")[:7]
    return render(request, "post_list.html", context={"post": post, "element": element, "title": title})



