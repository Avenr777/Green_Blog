from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .Blogs import Blog, Comment    
from mongoengine.errors import DoesNotExist
from datetime import datetime

def home(request):
    query = request.GET.get("q")

    if query:
        # 🔍 Search mode
        blogs = Blog.objects(
            title__icontains=query
        ).order_by("-created_at")[:6]

        trending_blogs = Blog.objects(
            likes__gt=0,
            title__icontains=query
        ).order_by("-likes", "-created_at")[:5]

    else:
        # 🏠 Normal homepage
        blogs = Blog.objects.order_by("-created_at")[:6]

        trending_blogs = Blog.objects(
            likes__gt=0
        ).order_by("-likes", "-created_at")[:5]

    return render(request, "index.html", {
        "blogs": blogs,
        "trending_blogs": trending_blogs,
        "query": query
    })

def register_view(request):
    form = UserCreationForm()

    if request.method == "POST": # If form is submitted
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    return render(request, "register.html", {"form": form})


# Login View
def login_view(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)    
            return redirect("home")

        else:
            # Form is invalid → incorrect username/password
            return render(request, "login.html", {
                "form": form,
                "error": "Incorrect username or password!"
            })

    return render(request, "login.html", {"form": form})

@login_required
def write_view(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        Blog(
            title=title,
            content=content,
            author=request.user.username
        ).save()
        print("Blog post created successfully!")

        return redirect("home")

    return render(request, "write.html")

# Logout View
def logout_view(request):
    logout(request)
    return redirect("home")

def read_view(request):

    return render(request, "read.html")
def post_view(request, blog_id):
    blog = Blog.objects.get(id=blog_id) #search for the blog with the given id

    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get("comment")

        if content:
            new_comment = Comment(
                user=request.user.username,
                content=content
            )
            blog.comments.append(new_comment)
            blog.save()

        return redirect("post_view", blog_id=blog.id)

    # Sort comments by newest first
    sorted_comments = sorted(
        blog.comments,
        key=lambda x: x.created_at,
        reverse=True
    )

    top_comments = sorted_comments[:2]
    remaining_comments = sorted_comments[2:]

    return render(request, "post_view.html", {
        "blog": blog,
        "top_comments": top_comments,
        "remaining_comments": remaining_comments
    })

@login_required
def like_blog(request, blog_id):
    blog = Blog.objects(id=blog_id).first()

    if blog:
        username = request.user.username

        # If user has NOT liked before
        if username in blog.liked_by:
            blog.update(
                pull__liked_by=username,
                dec__likes=1
            )
        else:
            blog.update(
                push__liked_by=username,
                inc__likes=1
            )
    return redirect("home")