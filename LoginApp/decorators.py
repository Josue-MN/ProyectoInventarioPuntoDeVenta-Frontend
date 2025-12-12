# decorators.py
from django.shortcuts import redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages

# ----------------------------------------------------------
# LOGIN REQUERIDO
# ----------------------------------------------------------
def login_requerido(funcion_envuelta):
    """
    Evita que un usuario no autenticado acceda a la vista.
    Solo verifica que exista 'Usuario_Username' y 'token' en la sesión.
    """
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def funcion_reemplazada(request, *args, **kwargs):
        usuario = request.session.get("Usuario_Username")
        token = request.session.get("token")

        # Si no hay usuario o token, redirige al login
        if not usuario or not token:
            try:
                messages.error(request, "Debes iniciar sesión.")
            except:
                pass  # Evita que falle si MessageMiddleware no está activo
            return redirect('Login')

        # Si hay sesión válida, ejecuta la vista original
        return funcion_envuelta(request, *args, **kwargs)

    return funcion_reemplazada


# ----------------------------------------------------------
# SOLO ADMIN
# ----------------------------------------------------------
def solo_admin(funcion_envuelta):
    """
    Permite acceso solo si el usuario logeado es 'Admin'.
    """
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def funcion_reemplazada(request, *args, **kwargs):
        usuario = request.session.get("Usuario_Username")
        token = request.session.get("token")

        # Verifica que exista sesión
        if not usuario or not token:
            try:
                messages.error(request, "Debes iniciar sesión.")
            except:
                pass
            return redirect('Login')

        # Solo Admin
        if usuario.lower() != "admin":
            try:
                messages.error(request, "No tienes permisos para acceder a esta sección.")
            except:
                pass
            return redirect('home')

        # Si es Admin, ejecuta la vista
        return funcion_envuelta(request, *args, **kwargs)

    return funcion_reemplazada
