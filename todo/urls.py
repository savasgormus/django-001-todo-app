from django.urls import path
from .views import home
from .views import todo_list, todo_add, todo_update, todo_delete

urlpatterns = [
    path("", home, name="home"),
    # path("list/", todo_list, name="list"),
    path("list/", todo_list.as_view(), name="list"),
    path("add/", todo_add.as_view(), name="add"),
    # path("update/<int:id>",todo_update, name="update"),
    path("update/<int:id>",todo_update.as_view(), name="update"),
    # path("delete/<int:id>",todo_delete,name="delete"),
    path("delete/<int:id>",todo_delete.as_view(),name="delete"),
]
