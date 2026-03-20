from django.urls import path

from . import views

urlpatterns = [
    path("movies/", views.index, name="movies"),
]
