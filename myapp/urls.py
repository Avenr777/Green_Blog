from django.urls import path
from . import views 
from django.shortcuts import redirect
urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('post/<str:blog_id>/', views.post_view, name='post_view'),
    path("write/", views.write_view, name="write"),
    path("like/<str:blog_id>/", views.like_blog, name="like_blog"),
]