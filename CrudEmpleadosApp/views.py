import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from LoginApp.decorators import solo_admin

API_URL = "http://127.0.0.1:8000/empleados/"  # Cambia según tu API

# ----------------------------------------------------------
# FUNCIÓN AUXILIAR: obtener headers con token
# ----------------------------------------------------------
def get_headers(request):
    token = request.session.get("token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}

# ----------------------------------------------------------
# LISTAR TODOS LOS EMPLEADOS
# ----------------------------------------------------------
@solo_admin
def empleadosData(request):
    try:
        headers = get_headers(request)
        response = requests.get(API_URL, headers=headers)

        if response.status_code == 401:
            messages.error(request, "No autorizado. Debes iniciar sesión nuevamente.")
            return redirect("Login")

        empleados = response.json()
    except Exception as e:
        print("ERROR LISTANDO EMPLEADOS:", e)
        empleados = []
        messages.error(request, "No se pudo conectar con la API.")

    return render(request, 'templateCrudEmpleado/empleados-models.html', {"Empleados": empleados})

# ----------------------------------------------------------
# REGISTRAR NUEVO EMPLEADO
# ----------------------------------------------------------
@solo_admin
def empleadoRegistrationView(request):
    if request.method == "GET":
        return render(request, 'templateCrudEmpleado/registro-empleado.html', {"data": {}, "errores": {}})

    data = {
        "RutEmpleado": request.POST.get("RutEmpleado"),
        "NombreEmpleado": request.POST.get("NombreEmpleado"),
        "ApellidoEmpleado": request.POST.get("ApellidoEmpleado"),
        "EdadEmpleado": request.POST.get("EdadEmpleado"),
        "NumeroTelefonoEmpleado": request.POST.get("NumeroTelefonoEmpleado"),
    }

    headers = get_headers(request)
    res = requests.post(API_URL, json=data, headers=headers)

    if res.status_code == 201:
        messages.success(request, "Empleado registrado correctamente")
        usuario = request.session.get('Usuario_Username')
        return redirect('admin-crud-empleado')

    try:
        errores = res.json()
    except:
        errores = {"general": ["Error desconocido"]}

    return render(request, 'templateCrudEmpleado/registro-empleado.html', {"data": data, "errores": errores})

# ----------------------------------------------------------
# ACTUALIZAR EMPLEADO
# ----------------------------------------------------------
@solo_admin
def actualizarEmpleado(request, IdEmpleado):
    headers = get_headers(request)

    if request.method == "GET":
        res = requests.get(f"{API_URL}{IdEmpleado}/", headers=headers)
        empleado = res.json() if res.status_code == 200 else {}
        return render(request, 'templateCrudEmpleado/registro-empleado.html', {"data": empleado, "errores": {}})

    data = {
        "RutEmpleado": request.POST.get("RutEmpleado"),
        "NombreEmpleado": request.POST.get("NombreEmpleado"),
        "ApellidoEmpleado": request.POST.get("ApellidoEmpleado"),
        "EdadEmpleado": request.POST.get("EdadEmpleado"),
        "NumeroTelefonoEmpleado": request.POST.get("NumeroTelefonoEmpleado"),
    }

    res = requests.put(f"{API_URL}{IdEmpleado}/", json=data, headers=headers)
    if res.status_code in (200, 202):
        messages.success(request, "Empleado actualizado correctamente")
        usuario = request.session.get('Usuario_Username')
        return redirect('admin-crud-empleado')

    try:
        errores = res.json()
    except:
        errores = {"general": ["Error desconocido"]}

    return render(request, 'templateCrudEmpleado/registro-empleado.html', {"data": data, "errores": errores})

# ----------------------------------------------------------
# DETALLE DE EMPLEADO
# ----------------------------------------------------------
@solo_admin
def detalleEmpleado(request, IdEmpleado):
    headers = get_headers(request)
    try:
        res = requests.get(f"{API_URL}{IdEmpleado}/", headers=headers)
        empleado = res.json() if res.status_code == 200 else {}
    except Exception as e:
        print("ERROR DETALLE EMPLEADO:", e)
        messages.error(request, "No se pudo obtener la información desde la API.")
        usuario = request.session.get('Usuario_Username')
        return redirect('admin-crud-empleado' if usuario == "Admin" else 'admin-crud-empleado')

    return render(request, 'templateCrudEmpleado/detalle-empleado.html', {"emp": empleado})

# ----------------------------------------------------------
# CONFIRMAR ELIMINACIÓN
# ----------------------------------------------------------
@solo_admin
def confirmarEliminar(request, IdEmpleado):
    headers = get_headers(request)
    res = requests.get(f"{API_URL}{IdEmpleado}/", headers=headers)
    empleado = res.json() if res.status_code == 200 else None
    return render(request, 'templateCrudEmpleado/confirmar-eliminar.html', {"emp": empleado})

# ----------------------------------------------------------
# ELIMINAR EMPLEADO
# ----------------------------------------------------------
@solo_admin
def eliminarEmpleado(request, IdEmpleado):
    if request.method != "POST":
        messages.error(request, "Método no permitido para eliminar empleados.")
        usuario = request.session.get('Usuario_Username')
        return redirect('admin-crud-empleado')

    headers = get_headers(request)
    res = requests.delete(f"{API_URL}{IdEmpleado}/", headers=headers)

    if res.status_code in (200, 204):
        messages.success(request, "Empleado eliminado correctamente")
    else:
        messages.error(request, f"No se pudo eliminar: {res.text}")

    usuario = request.session.get('Usuario_Username')
    return redirect('admin-crud-empleado')
