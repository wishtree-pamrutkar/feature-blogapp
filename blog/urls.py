from django.contrib import admin
from django.urls import path, include
from . import views
from .views import LikeView, AddPostView, UpdatePostView, DeletePostView

# app_name='blog'
urlpatterns = [
    path('postComment', views.postComment, name="postComment"),
    path('', views.blogHome, name="bloghome"),
    path('<str:slug>/<int:pk>', views.blogPost, name="blogPost"),
    path('like/<int:pk>/<str:slug>', views.LikeView, name='like_post'),
    # path('like/<str:sno>', views.LikeView, name='like_post')
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('blogPost/edit/<str:slug>/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('blogPost/<str:slug>/<int:pk>/remove', DeletePostView.as_view(), name='delete_post')

]
