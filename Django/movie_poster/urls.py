from django.urls import path
from . import views

urlpatterns = [
    path('poster/', views.upload_image, name='poster'),
]
