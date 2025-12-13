from django.shortcuts import render, redirect
from LoginApp.decorators import solo_admin

@solo_admin
def renderAdminHome(request):
    UsuarioLogeado = request.COOKIES.get("username", "Desconocido")
    return render(request, "templateAdminHome/adminhome.html", {"Usuario": UsuarioLogeado})



