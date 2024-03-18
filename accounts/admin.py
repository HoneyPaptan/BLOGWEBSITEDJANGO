from django.contrib import admin

# Register your models here.
from .models import Profile,Following,Category, Comment , Blog

admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Blog)