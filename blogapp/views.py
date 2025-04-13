# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import BlogPost  # make sure this is here!




def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            BlogPost.objects.create(user=request.user, title=title, content=content)

    posts = BlogPost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'posts': posts})


@login_required
def edit_post(request, post_id):
    # ✅ This line ensures only the post's owner can edit it
    post = get_object_or_404(BlogPost, id=post_id, user=request.user)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('dashboard')
    
    return render(request, 'edit_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    # ✅ Same here — this line prevents users from deleting others’ posts
    post = get_object_or_404(BlogPost, id=post_id, user=request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('dashboard')
    
    return render(request, 'delete_post.html', {'post': post})
