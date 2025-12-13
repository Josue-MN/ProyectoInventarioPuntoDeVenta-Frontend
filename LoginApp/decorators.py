from django.shortcuts import redirect
from django.views.decorators.cache import cache_control


# ----------------------------------------------------------
# LOGIN REQUERIDO
# ----------------------------------------------------------
def login_requerido(funcion_envuelta):
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def funcion_reemplazada(request, *args, **kwargs):
        token = request.COOKIES.get("token")
        username = request.COOKIES.get("username")

        if not token or not username:
            return redirect("Login")

        return funcion_envuelta(request, *args, **kwargs)

    return funcion_reemplazada


# ----------------------------------------------------------
# SOLO ADMIN
# ----------------------------------------------------------
def solo_admin(funcion_envuelta):
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def funcion_reemplazada(request, *args, **kwargs):
        token = request.COOKIES.get("token")
        username = request.COOKIES.get("username")

        if not token or not username:
            return redirect("Login")

        if username.lower() != "admin":
            return redirect("adminhome")

        return funcion_envuelta(request, *args, **kwargs)

    return funcion_reemplazada
