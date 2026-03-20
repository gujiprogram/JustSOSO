from django.urls import path
from app_auth import views

urlpatterns = [
    path('register/', views.Register.as_view()),
    path('login/', views.Login.as_view()),
    path('sendcode/', views.SendCode.as_view()),
]
