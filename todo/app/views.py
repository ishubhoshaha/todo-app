from django.shortcuts import render, redirect
from .models import todo
from django.contrib import messages

# Create your views here.

def home(request):
    if request.method == 'POST':
        try:
            task = request.POST['task']
            new_task = todo(name=task)
            new_task.save()
            messages.success(request, "Your task has been created successfully!")
        except Exception as E:
            messages.error(request, "Error Occured!")
    all_task = todo.objects.all()
    context = {'all_task': all_task}

    return render(request, 'todo/home.html', context)

def register(request):
    return render(request, 'todo/register.html', {})

def login(request):
    return render(request, 'todo/login.html', {})

def delete(request, id):
    try:
        todo.objects.filter(id=id).delete()
        messages.error(request, "Deleted Successfully!")
    except Exception as E:
        messages.error(request, "Error Occured!! Can't delete your task.")
    return redirect(home)

def update(request, id):
    try:
        task = todo.objects.filter(id=id)
        if task.first().status == True:
            task.update(status=False)
            messages.success(request, "Task back to your bucket!")
        else:
            task.update(status=True)
            messages.success(request, "Bingo! Task Completed.")

    except Exception as E:
        messages.error(request, "Error! Can't update your task.")

    return redirect(home)