from django.urls import path
from . import views
from .views import LoginView, Register

urlpatterns = [
    path('register/', Register.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login")
]