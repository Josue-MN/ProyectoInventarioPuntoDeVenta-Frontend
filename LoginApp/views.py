import requests
from django.shortcuts import render, redirect

import requests
from django.shortcuts import render, redirect

API_LOGIN_URL = "http://127.0.0.1:8000/api/token/"


def renderlogin(request):
    return render(request, "templateLogin/login.html")


def renderLoginForm(request):
    if request.method == "POST":
        username = request.POST.get("UsernameField")
        password = request.POST.get("PasswordField")

        if not username or not password:
            return render(
                request,
                "templateLogin/login-form.html",
                {"error": "Debe ingresar usuario y contraseña."}
            )

        data = {
            "username": username,
            "password": password
        }

        try:
            response = requests.post(API_LOGIN_URL, data=data, timeout=5)
        except requests.RequestException:
            return render(
                request,
                "templateLogin/login-form.html",
                {"error": "No se pudo conectar con el servidor de autenticación."}
            )

        if response.status_code == 200:
            access_token = response.json().get("access")

            if not access_token:
                return render(
                    request,
                    "templateLogin/login-form.html",
                    {"error": "La API no devolvió un token válido."}
                )

            redirect_response = redirect(
                "adminhome" if username.lower() == "admin" else "home"
            )

            redirect_response.set_cookie(
                "token",
                access_token,
                httponly=True,
                samesite="Lax"
            )

            redirect_response.set_cookie(
                "username",
                username,
                samesite="Lax"
            )

            return redirect_response

        return render(
            request,
            "templateLogin/login-form.html",
            {"error": "Usuario o contraseña incorrectos."}
        )

    return render(request, "templateLogin/login-form.html")


def renderLogout(request):
    response = redirect("Login")
    response.delete_cookie("token")
    response.delete_cookie("username")
    return response
