from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from app.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Користувач вже існує")
        else:
            user = CustomUser.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, "Реєстрація успішна")
            return redirect("login")

    return render(request, "register.html",{"user": request.user})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("register")  # Перенаправити кудись після входу
        else:
            messages.error(request, "Невірні дані")

    return render(request, "login.html",{"user": request.user})

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def home(request):
    return render(request, "home.html", {"user": request.user})