import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from LoginApp.decorators import login_requerido, solo_admin

API_URL = "http://127.0.0.1:8000/bodegas/"

# ----------------------------------------------------------
# FUNCIÓN PARA OBTENER HEADERS CON TOKEN
# ----------------------------------------------------------
def get_headers(request):
    token = request.session.get("token")

    # Si no hay token, no pedirá nada a la API
    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}"
    }



# Vista para mostrar todos los cargos en una tabla/listado
@solo_admin
def cargosData(request):
    cargos = Cargos.objects.all()  # Obtiene todos los registros del modelo Cargos
    data = {'Cargos': cargos}  # Diccionario con los cargos para enviarlos a la plantilla
    return render(request, 'templateCrudCargo/cargos-models.html', data)  # Renderiza la plantilla con los datos


# Vista para registrar un nuevo cargo
@solo_admin
def cargosRegistracionView(request):
    form = forms.CargoRegistracionForm()  # Crea un formulario vacío

    if request.method == 'POST':  # Si se envía el formulario
        form = forms.CargoRegistracionForm(request.POST)  # Carga los datos enviados
        if form.is_valid():  # Valida los datos del formulario
            # Imprime en consola los datos ingresados (útil para depuración)
            print("FORM VALIDO")
            print("TIPO DE CARGO: ", form.cleaned_data['TipoDeCargo'])
            print("ESTADO DEL CARGO: ", form.cleaned_data['EstadoDelCargo'])
            print("DESCRIPCION DEL CARGO: ", form.cleaned_data['DescripcionDelCargo'])
            print("SUELDO BASE: ", form.cleaned_data['SueldoBase'])

            cargo_nuevo = form.save()  # Guarda el cargo en la base de datos
            RegistrarAuditoriaCargo(request, cargo_nuevo, "REGISTRAR")
            messages.success(request, "Cargo registrado correctamente")  # Mensaje de éxito
            return redirect('admin-crud-cargo')  # Redirige al listado de cargos
        else:
            messages.error(request, "Corrige los errores en el formulario antes de continuar")  # Mensaje de error

    data = {'form': form}  # Diccionario con el formulario (vacío o con errores)
    return render(request, 'templateCrudCargo/registro-cargo.html', data)  # Renderiza el formulario


# Vista para actualizar un cargo existente
@solo_admin
def actualizarCargo(request, IdCargos):
    cargo = Cargos.objects.get(IdCargos=IdCargos)  # Obtiene el cargo por su ID
    form = forms.CargoRegistracionForm(instance=cargo)  # Crea un formulario con los datos existentes

    if request.method == 'POST':  # Si se envía el formulario con cambios
        form = forms.CargoRegistracionForm(request.POST, instance=cargo)  # Carga los datos actualizados
        if form.is_valid():  # Valida los datos
            cargo_actualizado = form.save()  # Guarda los cambios
            RegistrarAuditoriaCargo(request, cargo_actualizado, "ACTUALIZAR")
            messages.success(request, "Cargo actualizado correctamente")  # Mensaje de éxito
            return redirect('admin-crud-cargo')  # Redirige al listado
        else:
            messages.error(request, "Corrige los errores en el formulario antes de continuar")  # Mensaje de error

    data = {'form': form}  # Diccionario con el formulario
    return render(request, 'templateCrudCargo/registro-cargo.html', data)  # Renderiza el formulario


# Vista para mostrar confirmación antes de eliminar un cargo
@solo_admin
def confirmarEliminar(request, IdCargos):
    cargo = Cargos.objects.get(IdCargos=IdCargos)  # Obtiene el cargo por su ID
    data = {'cag' : cargo}  # Diccionario con el cargo
    return render(request, 'templateCrudCargo/confirmar-eliminar.html', data)  # Renderiza plantilla de confirmación


# Vista para eliminar un cargo
@solo_admin
def eliminarCargo(request, IdCargos):
    cargo = Cargos.objects.get(IdCargos=IdCargos)  # Obtiene el cargo por su ID
    if request.method == 'POST':  # Solo permite eliminar si se envía POST
        RegistrarAuditoriaCargo(request, cargo, "ELIMINAR")
        cargo.delete()  # Elimina el registro de la base de datos
        messages.success(request, f"El cargo '{cargo.TipoDeCargo}' fue eliminado correctamente.")  # Mensaje de éxito
        return redirect('admin-crud-cargo')  # Redirige al listado
    else:
        messages.error(request, "Método no permitido para eliminar usuarios.")  # Mensaje si no es POST
        return redirect('admin-crud-cargo')  # Redirige al listado


# Vista para mostrar los detalles de un cargo específico
@solo_admin
def detalleCargo(request, IdCargos):
    cargo = Cargos.objects.get(IdCargos=IdCargos)  # Obtiene el cargo por su ID
    data = {'cag' : cargo}  # Diccionario con el cargo
    return render(request, 'templateCrudCargo/detalle-cargo.html', data)  # Renderiza plantilla de detalle
