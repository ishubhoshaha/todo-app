from django.shortcuts import render, redirect
from .models import todo
from django.contrib import messages


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def home(request):
    if request.method == 'POST':
        new_task = todo(name=request.POST['task'])
        new_task.save()
        messages.success(request, "Your task has been saved!")
    all_task = todo.objects.all()
    context = {
        'all_task': all_task
    }
    return render(request, 'todo/home.html', context)

def update(request, id):
    task = todo.objects.filter(id=id)
    if task.first().status == True:
        task.update(status=False)
    else:
        task.update(status=True)
    return redirect(home)


def delete(request, id):
    todo.objects.filter(id=id).delete()
    return redirect(home)

def login_view(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        asdf = authenticate(request, username=username, password=password)
        if asdf is not None:
            login(request, asdf)
            messages.success(request,"Successfully Login")
            return redirect(home)
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'todo/login.html', {})


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('login')


def register_view(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        confirm_pass = request.POST['confirm-password']
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            messages.error(request, "username already taken")
        elif password != confirm_pass:
            messages.error(request, "Password does not match")
        else:
            new_user = User.objects.create_user(username=username, email=email,password=password)
            new_user.save()
            return redirect('login')

        print(request.POST)
    return render(request, 'todo/register.html', {})