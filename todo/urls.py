from django.urls import path
from .views import home, todo_delete, todo_list, todo_create, todo_update

urlpatterns = [
    path("", home, name="home"),
    path("list/", todo_list, name="list"),
    path("add/", todo_create, name="add"),
    path("update/<int:id>/", todo_update, name="update"),
    path("delete/<int:id>/", todo_delete, name="delete")
]
