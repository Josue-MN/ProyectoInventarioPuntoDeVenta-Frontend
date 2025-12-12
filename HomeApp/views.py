from django.shortcuts import render
from LoginApp.decorators import login_requerido

@login_requerido
def renderTemplateHome(request):

    UsuarioLogeado = request.session.get("Usuario_Username")

    data = {
        'Usuario': UsuarioLogeado
    }

    return render(request, "templateHome/home.html", data)

