
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from home.views import signup_redirect
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("home.urls")),
    path("account/", include("accounts.urls")),
    path("leaderboard/", include("leaderboard.urls")),
    path('accounts/', include('allauth.urls')),
    path('accounts/social/signup/', signup_redirect, name='signup_redirect'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)