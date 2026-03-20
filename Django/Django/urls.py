from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('', include('restfulapi.urls')),
                  path('', include('users.urls')),
                  path('', include('movies.urls')),
                  path('', include('app_auth.urls')),
                  path('', include('movie_poster.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
