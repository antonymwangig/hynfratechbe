
from django.urls import path,include
from .views import GoogleLoginAPIView, UserLoginAPIView 

urlpatterns = [
    path('google-login/', GoogleLoginAPIView.as_view()),
    path('login/', UserLoginAPIView.as_view()),

]
