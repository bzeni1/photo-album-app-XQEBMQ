from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm

@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("photo_list")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data.get("email") or "",
            password=form.cleaned_data["password1"],
        )
        login(request, user)
        return redirect("photo_list")

    return render(request, "album/register.html", {"form": form})



@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("photo_list")

    error = None
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is None:
            error = "Hibás felhasználónév/jelszó."
        else:
            login(request, user)
            return redirect("photo_list")
    return render(request, "album/login.html", {"error": error})



def logout_view(request):
    logout(request)
    return redirect("photo_list")