

from django.urls import path

from . import views
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('accounts/google/login/', views.custom_google_login, name='custom_google_login'),
  
    

]
