from django.shortcuts import render, redirect
from django.contrib import messages
from AuditoriaApp.views import RegistrarAuditoriaUsuario
from LoginApp.decorators import solo_admin

#Models
@solo_admin
def usuariosData(request):
    """
    Vista que muestra el listado completo de usuarios del sistema.
    El decorador @solo_admin asegura que solo administradores puedan acceder.
    """
    usuarios = Usuarios.objects.all()  # Obtiene todos los usuarios registrados
    data = {'Usuarios' : usuarios}     # Datos enviados al template
    return render(request, 'templateCrudUsuario/usuarios-models.html', data)


#Form
@solo_admin
def usuariosRegistrationView(request):
    """
    Vista encargada del registro de un nuevo usuario.
    Muestra el formulario de creación y procesa la información enviada.
    """
    form = forms.UsuarioRegistrationForm()  # Formulario vacío para renderizar
    actualizar = False                       # Indica que NO es actualización, sino registro

    # Si el método es POST, significa que el formulario fue enviado
    if request.method == 'POST':
        form = forms.UsuarioRegistrationForm(request.POST)
        
        # Validación del formulario
        if form.is_valid():
            # Debug (opcional) para ver los datos procesados
            print("FORM ES VALIDO")
            print("USERNAME: ", form.cleaned_data['Username'])
            print("PASSWORD: ", form.cleaned_data['Password'])
            print("CONFIRMAR PASSWORD: ", form.cleaned_data['ConfirmarPassword'])
            print("CORREO ELECTRONICO: ", form.cleaned_data['CorreoElectronico'])
            print("EMPLEADO SELECCIONADO", form.cleaned_data['Empleado'])
            print("CARGO SELECCIONADO", form.cleaned_data['Cargo'])
            
            # Guarda el usuario en la BD
            usuario_registrado = form.save()

            # Registra la auditoría correspondiente
            RegistrarAuditoriaUsuario(request, usuario_registrado, "REGISTRAR")

            # Mensaje de éxito para el usuario
            messages.success(request, "Usuario registrado correctamente")

            # Redirección al listado de usuarios
            return redirect('admin-crud-usuario')

        else:
            # Si hay errores en el formulario
            messages.error(request, "Corrige los errores en el formulario antes de continuar")
        
    # Renderiza la vista enviando el formulario
    data = {
        'form': form,
        'actualizar': actualizar
    }
    return render(request, 'templateCrudUsuario/registro-usuario.html', data)


#Actualizar
@solo_admin
def actualizarUsuario(request, IdUsuarios):
    """
    Vista para actualizar un usuario existente.
    Carga el formulario con los datos actuales del usuario.
    """
    usuario = Usuarios.objects.get(IdUsuarios=IdUsuarios)  # Obtiene el usuario por ID
    form = forms.UsuarioUpdateForm(instance=usuario)        # Formulario cargado con sus datos
    actualizar = True                                       # Indica que esta acción es de actualización

    if request.method == 'POST':
        form = forms.UsuarioUpdateForm(request.POST, instance=usuario)
        
        if form.is_valid():
            usuario_actualizado = form.save()  # Guarda los cambios
            RegistrarAuditoriaUsuario(request, usuario_actualizado, "ACTUALIZAR")
            messages.success(request, "Usuario actualizado correctamente")
            return redirect('admin-crud-usuario')
        else:
            messages.error(request, "Corrige los errores en el formulario antes de continuar")
            
    data = {
        'form': form,
        'actualizar': actualizar,
        'UsuarioActual': usuario
    }
    return render(request, 'templateCrudUsuario/registro-usuario.html', data)


#Eliminar
@solo_admin
def confirmarEliminar(request, IdUsuarios):
    """
    Vista que muestra una confirmación antes de eliminar un usuario.
    Esto evita eliminaciones accidentales.
    """
    usuario = Usuarios.objects.get(IdUsuarios=IdUsuarios)
    data = {'usu' : usuario}
    return render(request, 'templateCrudUsuario/confirmar-eliminar.html', data)


@solo_admin
def eliminarUsuario(request, IdUsuarios):
    """
    Vista que realiza la eliminación real del usuario.
    Solo permite el método POST como medida de seguridad.
    """
    usuario = Usuarios.objects.get(IdUsuarios=IdUsuarios)

    if request.method == 'POST':
        # Registra la auditoría antes de eliminar
        RegistrarAuditoriaUsuario(request, usuario, "ELIMINAR")

        usuario.delete()  # Elimina el usuario
        messages.success(request, f"El usuario '{usuario.Username}' fue eliminado correctamente.")

        return redirect('admin-crud-usuario')

    else:
        # Si alguien intenta eliminar mediante GET, se bloquea por seguridad
        messages.error(request, "Método no permitido para eliminar usuarios.")
        return redirect('admin-crud-usuario')


#Detalle
@solo_admin
def detalleUsuario(request, IdUsuarios):
    """
    Vista que muestra el detalle completo de un usuario específico.
    """
    usuario = Usuarios.objects.get(IdUsuarios=IdUsuarios)
    data = {'usu' : usuario}
    return render(request, 'templateCrudUsuario/detalle-usuario.html', data)


