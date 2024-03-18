from django.shortcuts import render
from accounts.models import Blog
# Create your views here.
import re
import math
def calculate_read_time(content, wpm=200):
    words = re.findall(r'\w+', content)
    num_words = len(words)
    read_time = num_words / wpm
    return math.ceil(read_time)
def leaderboard(request):
    blogs_by_views = Blog.objects.order_by('-view_count')
    for blog in blogs_by_views:
        read_time = calculate_read_time(blog.content)
        blog.read_time = read_time

    return render(request, "leaderboard/index.html", {"blogs": blogs_by_views})