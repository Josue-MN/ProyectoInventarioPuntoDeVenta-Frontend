from django.shortcuts import render
from LoginApp.decorators import login_requerido

@login_requerido
def renderTemplateHome(request):
    UsuarioLogeado = request.COOKIES.get("username", "Desconocido")
    return render(request, "templateHome/home.html", {"Usuario": UsuarioLogeado})

