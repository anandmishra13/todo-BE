from django.urls import path, include
from . import views


urlpatterns = [
    path('create/', views.create_todo, name='todo_create'),
    path('get/', views.get_todo, name='todo_get'),
]