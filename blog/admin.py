# from django.contrib import admin
# from blog.models import Post
#
# admin.site.register(Post)Post
# Register your models here.
from django.contrib import admin
from blog.models import Post, BlogComment, Category



admin.site.register((Post, BlogComment, Category))
