
from django.urls import path,include
from .views import GoogleLoginAPIView, UserLoginAPIView,SignupAPIView

urlpatterns = [
    path('sign-up/', SignupAPIView.as_view(), name="sign-up"),
    path('login/', UserLoginAPIView.as_view() ,name="login"),
    path('google-login/', GoogleLoginAPIView.as_view()),
    

]
