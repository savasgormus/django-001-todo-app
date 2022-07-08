from django.shortcuts import render
from django.http import HttpResponse
from .models import Todo

# Create your views here.


def home(request):
    return render(request, "todo/home.html")

def todo_list(request):
    todos = Todo.objects.all()
    context = {
        'todos' : todos
    }
    return render(request, 'todo_list.html', context)

def todo_create(request):
    pass

def todo_update(request, id):
    pass

def todo_delete(request, id):
    pass