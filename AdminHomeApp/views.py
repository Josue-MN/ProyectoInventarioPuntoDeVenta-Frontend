from django.shortcuts import render, redirect
from LoginApp.decorators import solo_admin

@solo_admin
def renderAdminHome(request):
    """
    Vista del panel de administración.
    Lee el usuario que inició sesión desde la sesión del frontend.
    """

    # Obtener datos del usuario desde la sesión
    usuario_username = request.session.get("Usuario_Username")
    token = request.session.get("token")

    # Seguridad básica: si no hay sesión válida
    if not usuario_username or not token:
        return redirect("login")

    # Contexto enviado al template
    context = {
        "Usuario": usuario_username
    }

    return render(
        request,
        "templateAdminHome/adminhome.html",
        context
    )



