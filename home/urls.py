

from django.urls import path

from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("change_image/<str:username>/", views.change_image, name="change_image"),
   
    path('savecommet/<int:pk>/', views.save_commet, name='save_commet'),
    path('blogs/<int:pk>/', views.blog_view, name='blog_view'),
    path('delete/<int:pk>/', views.delete_blog, name='delete_blog'),
    path('blogs/<int:pk>/save-unsave/', views.save_unsave_blog, name='save_unsave_blog'),
    path("write/", views.write_blog ,name="write")

]
