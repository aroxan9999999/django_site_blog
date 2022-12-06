from django.urls import path, include
from .views import *
from rest_framework import routers
router = routers.SimpleRouter()
router.register("post", Postapi)
router.register("category", Catefory_api)
router.register("user", User_api)

print(router.urls)

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("v1_all/", include(router.urls)),
    path("v2_post_all/", Post_list.as_view()),
    path("v2_category_all/", Catefory_list.as_view()),
]

'''
http://127.0.0.1:8000/api/v1_all/user
http://127.0.0.1:8000/api/v1_all/category
http://127.0.0.1:8000/api/v1_all/post
http://127.0.0.1:8000/api/v2_post_all
http://127.0.0.1:8000/api/v2_category_all/
http://127.0.0.1:8000/api/auth/login
http://127.0.0.1:8000/api/auth/logout
'''