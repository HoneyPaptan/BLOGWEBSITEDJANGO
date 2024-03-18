from django.shortcuts import render, redirect,HttpResponseRedirect
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Following
from django.http import JsonResponse
from accounts.models import Blog,Category,Comment,Profile
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib import messages

# Create your views here.

import re
import math
def home(request):
    latest_blogs = Blog.objects.order_by('-timestamp')[:3]
    for blog in latest_blogs:
        read_time = calculate_read_time(blog.content)
        blog.read_time = read_time
        blog.title = blog.title.capitalize()

    return render(request, "home/home.html", {"latest_blogs": latest_blogs})

def calculate_read_time(content, wpm=200):
    words = re.findall(r'\w+', content)
    num_words = len(words)
    read_time = num_words / wpm
    return math.ceil(read_time)



def profile(request, username):
    if not request.user.is_authenticated:
        return redirect('login')
    user = get_object_or_404(User, username=username)
    if user.is_superuser:
        return redirect("home")

    # Fetch the profile of the user whose profile is being viewed
    profile = get_object_or_404(Profile, user=user)

    is_google_user = False
    profile_pic = None

    # Fetch user's profile picture
    if user.socialaccount_set.filter(provider='google').exists():
        try:
            social_account = SocialAccount.objects.get(user=user, provider='google')
            profile_pic = social_account.extra_data.get('picture')
            is_google_user = True
        except SocialAccount.DoesNotExist:
            pass  # Handle exception if necessary
    elif profile.profile_picture:
        profile_pic = profile.profile_picture.url

    user_blog = Blog.objects.filter(author=user)
    saved_blogs = user.saved_blogs.all()

    for saved_blog in saved_blogs:
        read_time = calculate_read_time(saved_blog.content)
        saved_blog.read_time = read_time

    for blog in user_blog:
        read_time = calculate_read_time(blog.content)
        blog.read_time = read_time

    # Check if the current user is following the profile user
    is_following = request.user.is_authenticated and Following.objects.filter(
        follower=request.user,
        followed_user=user
    ).exists()

    # Get the number of followers for the profile user
    num_followers = user.followers.count()

    # Determine if viewing own profile
    is_own_profile = request.user == user

    # Handle follow/unfollow action
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'follow':
            # Follow the user
            Following.objects.create(follower=request.user, followed_user=user)
            return HttpResponseRedirect(request.path_info)
        elif action == 'unfollow':
            # Unfollow the user
            Following.objects.filter(follower=request.user, followed_user=user).delete()
            return HttpResponseRedirect(request.path_info)

    return render(request, "home/profile.html", {
        "profile_pic": profile_pic,
        "user": user,
        "is_following": is_following,
        "num_followers": num_followers,
        "user_blog": user_blog,
        "saved_blogs": saved_blogs if is_own_profile else None,
        'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
        "is_google_user": is_google_user,
        "is_own_profile": is_own_profile,
    })

def signup_redirect(request):
    
    return redirect("home")

def change_image(request, username):
    if request.method == "POST":
        profile_picture = request.POST.get("image")
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.profile_picture = profile_picture
        profile.save()
    messages.success(request, "Profile Pic changed!!")
    return redirect("profile", username = username)
    
def blog_view(request, pk):
    blog = Blog.objects.get(pk=pk)
    
    # Increment view count
    blog.view_count += 1
    blog.save()  # Save the updated view count
    
    author = blog.author
    
    # Get profile picture if available
    profile_image = None
    if hasattr(author, 'socialaccount'):
        profile_image = author.socialaccount.extra_data.get('picture')
    
    # Check if the current user is following the author
    is_following = request.user.is_authenticated and Following.objects.filter(follower=request.user, followed_user=author).exists()
    
    # Handle follow/unfollow action
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'follow':
            # Follow the author
            Following.objects.create(follower=request.user, followed_user=author)
        elif action == 'unfollow':
            # Unfollow the author
            Following.objects.filter(follower=request.user, followed_user=author).delete()

        # Redirect back to the same blog detail page
        return redirect('blog_view', pk=pk)
    
    # Check if the blog post is saved by the user
    is_saved = request.user.is_authenticated and request.user.saved_blogs.filter(pk=pk).exists()
    
    return render(request, "home/blogdetail.html", {
        "blog": blog,
        "profile_image": profile_image,
        "is_following": is_following,
        "is_saved": is_saved,
    })
@login_required
def save_unsave_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    if request.method == 'POST':
        if request.user in blog.saves.all():
            # Unsave the blog
            blog.saves.remove(request.user)
            is_saved = False
        else:
            # Save the blog
            blog.saves.add(request.user)
            is_saved = True
        
        return JsonResponse({'is_saved': is_saved})

@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, id=pk)

    # Check if the logged-in user is the author of the blog post
    if request.user == blog.author:
        # Delete the blog post
        blog.delete()
        messages.success(request, "Blog deleted !!")

        return redirect("profile", username = request.user)
   

    return redirect('home')


@login_required
def write_blog(request):
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")
        image_url = request.POST.get("image_url")
        author = request.user
        category_name = request.POST.get("category")
        new_category_name = request.POST.get("new_category")

        # Ensure that a category is provided
        if not category_name and not new_category_name:
           
            return redirect('write')

        try:
            # Check if the blog with the same title or content already exists
            existing_blog = Blog.objects.filter(title=title) | Blog.objects.filter(content=content)
            if existing_blog.exists():
                return redirect('write')

            # Check if the selected category exists or create a new one
            if category_name:
                category, created = Category.objects.get_or_create(name=category_name)
            else:
                category, created = Category.objects.get_or_create(name=new_category_name)

            # Create a new blog instance with the category
            new_blog = Blog.objects.create(
                title=title,
                content=content,
                author=author,
                category=category,
                blog_main_image=image,
                image_url=image_url
            )
            new_blog.save()
            messages.success(request, "Blog created. check it out in home or profile!")


            return redirect('home')
        except Exception as e:
            messages.error(request, "Error occurred while creating check the title maybe you have a matching title with other blogs!")

           
            return redirect('write')

    return render(request, "home/write.html", {"categories": categories})

def save_commet(request, pk):
    blog = Blog.objects.get(pk=pk)
    if request.method == 'POST':
        content  = request.POST.get("content")
        user = request.user
        blog = blog
        comments = Comment(content = content, user = user , blog = blog)
        comments.save()
        messages.success(request, "Saved!")

        return redirect("blog_view", pk = pk)
    
   
    
    return render(request, "home/blogdetail.html")

def about(request):
    return render(request, "home/about.html")