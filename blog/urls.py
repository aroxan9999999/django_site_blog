from django.urls import path
from .views import *

urlpatterns = [
    path("post_list", post_list, name="post_list"),
    path("post_detail/<int:post_pk>", post_detail, name="post_detail"),
    path("post_detail/<int:post_pk>/comment/", comment_post, name="coment_post"),
    path("new_post", new_post, name="new_post"),
    path("update_post/<int:post_pk>", post_update, name="update_post"),
    path("delete_post/<int:post_pk>", post_delete, name="delete_post"),
    path("top_post", top_post, name="top_post"),
    path("category", category, name="category"),
    path("category/<str:name>", category_post, name="category_post"),
    path("user_post/<str:user_name>", user_post, name="user_post"),
    path("post_delete/<int:post_pk>", post_delete, name="post_delete"),
    path("post_publish/<int:post_pk>", post_publish, name="post_publish"),
]
