from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    verified = models.BooleanField(default=False) 
    def __str__(self):
        return self.user.username

class Following(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed_user')

class Category(models.Model):
    name = models.CharField(max_length=300, default = "")

    def __str__(self):
        return self.name
    
class Blog(models.Model):
    title = models.CharField(max_length=200, default="", blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Update ForeignKey to use on_delete
    image_url = models.URLField(max_length = 300, default = "", blank=True, null=True)
    blog_main_image = models.ImageField(upload_to= "blogmain/" , default="", null=True, blank=True)
    # New fields for likes, comments, and saves
    view_count = models.IntegerField(default=0, editable=False)
    comments = models.ManyToManyField(User, through='Comment', related_name='commented_blogs', blank=True)
    saves = models.ManyToManyField(User, related_name='saved_blogs', blank=True)
    
   

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"


