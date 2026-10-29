from django.shortcuts import redirect, render
from .models import Movie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import requests
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    response = requests.get("https://omdbapi.com/?apikey=38b4b85b&s=Batman&type=movie")
    results_json = response.json()
    movies = results_json["Search"]
    context = {
        "movies": movies
    }
    return render(request, 'index.html', context )

@login_required
def home2(request):
    movies = Movie.objects.all()
    return render(request, "home.html", {"movies" : movies})

def create_user(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password=request.POST["password"]
        )
        user.save()
        return redirect("home2")
    return render(request, "register.html")
context = {"action": "Adicionar"}

def login_user(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("home2")
        return render(request, "login.html", {"erro": "Usuário ou senha inválidos."})

    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("login")