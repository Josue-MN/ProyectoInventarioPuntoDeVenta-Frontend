from django.shortcuts import render
from LoginApp.decorators import login_requerido

@login_requerido
def renderAdminHome(request):
    # Tomamos el username desde la sesión
    UsuarioLogeado = request.session.get('Usuario_Username')

    # Creamos el contexto sin consultar ninguna base de datos
    data = {'Usuario': UsuarioLogeado}

    return render(request, 'templateAdminHome/adminhome.html', data)



