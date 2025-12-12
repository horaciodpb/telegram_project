from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
#from django.contrib.auth.models import User
from django.contrib import messages

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validación simple
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese usuario ya existe.")
            return redirect("register_view")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Ese email ya está registrado.")
            return redirect("register_view")

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Cuenta creada correctamente. Ahora inicia sesión.")
        return redirect("login")

    return render(request, "accounts/register.html")

'''
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Cuenta creada. Ahora iniciá sesión.")
        return redirect('login')

    return render(request, "accounts/register.html")
'''