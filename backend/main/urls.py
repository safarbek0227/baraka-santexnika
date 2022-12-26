from django.urls import path
from .import views

app_name = "main"

urlpatterns = [
    path("", views.HomeView , name="home"),
    path("GetTodos/", views.workWithTodo , name="GetTodos"),
    path("todos/", views.todoView , name="todos"),

]
