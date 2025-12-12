import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_LOGIN_URL = "http://127.0.0.1:8000/api/token/"


def renderlogin(request):
    return render(request, 'templateLogin/login.html')


def renderLoginForm(request):
    if request.method == "POST":
        username = request.POST.get("UsernameField")
        password = request.POST.get("PasswordField")

        # Datos a enviar a la API
        data = {
            "username": username,
            "password": password
        }

        # Enviar request al backend (API)
        response = requests.post(API_LOGIN_URL, data=data)

        # Si la API dice que las credenciales son correctas
        if response.status_code == 200:
            json_data = response.json()
            access_token = json_data.get("access")

            if not access_token:
                messages.error(request, "La API no devolvió un token de acceso.")
                return render(request, "templateLogin/login-form.html")

            # Guardar token en sesión
            request.session["token"] = access_token
            request.session["Usuario_Username"] = username

            # Behavior personalizado
            if username.lower() == "admin":
                return redirect("adminhome")
            else:
                return redirect("home")

        # Si la API responde error de credenciales
        messages.error(request, "Usuario o contraseña incorrectos.")
        return render(request, "templateLogin/login-form.html")

    # Si entra por GET, mostrar formulario normal
    return render(request, "templateLogin/login-form.html")


def renderLogout(request):
    request.session.flush()
    return redirect('Login')