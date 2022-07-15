from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView , CreateView , UpdateView , DeleteView
from .forms import TodoForm

from todo.models import Todo

# Create your views here.


def home(request):
    return render(request, "todo/home.html")

#! list function based
# def todo_list(request):
#     todos = Todo.objects.all()
#     context = {
#         'todos' : todos
#     }
#     return render(request,"todo/todo_list.html", context)

class todo_list(ListView):
    model= Todo
    context_object_name = "todos"
    template_name = "todo/todo_list.html"

#! create function based
# def todo_add(request):
#     form = TodoForm()
#     if request.method == "POST":
#         form = TodoForm(request.POST)
#         if form.is_valid:
#             form.save()
#         return redirect("list")
#     context = {
#         "form" : form
#     }
#     return render(request, "todo/todo_add.html", context)

class todo_add(CreateView):
    model = Todo
    from_class = TodoForm
    fields = "__all__"
    template_name = "todo/todo_add.html"
    success_url = reverse_lazy("list")

#! update function base
# def todo_update(request, id):
#     todo = Todo.objects.get(id=id)
#     form = TodoForm(instance=todo)

#     if request.method == "POST":
#         form = TodoForm(request.POST, instance=todo)
#         if form.is_valid:
#             form.save()
#         return redirect("list")
#     context = {
#         "todo" : todo,
#         "form" : form
#     }
#     return render(request, "todo/todo_update.html",context)

class todo_update(UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = "todo/todo_update.html"
    success_url = reverse_lazy("list")
    pk_url_kwarg = 'id'

#! delete function base
# def todo_delete(request, id):
#     todo = Todo.objects.get(id=id)
#     if request.method == "POST":
#         todo.delete()
#         return redirect("list")
#     context = {
#         "todo" : todo
#     }
#     return render(request, "todo/todo_delete.html", context)

class todo_delete(DeleteView):
    model = Todo
    template_name = "todo/todo_delete.html"
    success_url = reverse_lazy("list")
    pk_url_kwarg = 'id'



