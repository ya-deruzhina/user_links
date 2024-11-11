from django.urls import path

from .views import *


urlpatterns = [
    path('users/sign_in/', SignInView.as_view()),
    path('users/about/', AboutUserView.as_view()),
    path('users/registration/', UserRegistrationView.as_view()),
    path('users/update/', UserUpdateView.as_view()),
]
