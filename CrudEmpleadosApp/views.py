import requests
from django.shortcuts import render, redirect
from LoginApp.decorators import solo_admin

API_URL = "http://127.0.0.1:8000/empleados/"  # Cambia según tu API


# ----------------------------------------------------------
# HEADERS JWT
# ----------------------------------------------------------
def get_headers(request):
    token = request.COOKIES.get("token")
    if not token:
        return None
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


# ----------------------------------------------------------
# LISTAR EMPLEADOS
# ----------------------------------------------------------
@solo_admin
def empleadosData(request):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        res = requests.get(API_URL, headers=headers)
        if res.status_code == 401:
            return redirect("Login")
        empleados = res.json()
    except Exception as e:
        print("ERROR LISTANDO EMPLEADOS:", e)
        empleados = []

    return render(request, 'templateCrudEmpleado/empleados-models.html', {"Empleados": empleados})


# ----------------------------------------------------------
# REGISTRAR NUEVO EMPLEADO
# ----------------------------------------------------------
@solo_admin
def empleadoRegistrationView(request):
    if request.method == "GET":
        return render(request, 'templateCrudEmpleado/registro-empleado.html', {"data": {}, "errores": {}})

    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    data = {
        "RutEmpleado": request.POST.get("RutEmpleado"),
        "NombreEmpleado": request.POST.get("NombreEmpleado"),
        "ApellidoEmpleado": request.POST.get("ApellidoEmpleado"),
        "EdadEmpleado": request.POST.get("EdadEmpleado"),
        "NumeroTelefonoEmpleado": request.POST.get("NumeroTelefonoEmpleado"),
    }

    try:
        res = requests.post(API_URL, json=data, headers=headers)
        if res.status_code == 201:
            return redirect('admin-crud-empleado')
        errores = res.json()
    except Exception as e:
        print("ERROR REGISTRANDO EMPLEADO:", e)
        errores = {"general": ["No se pudo conectar con la API"]}

    return render(request, 'templateCrudEmpleado/registro-empleado.html', {"data": data, "errores": errores})


# ----------------------------------------------------------
# ACTUALIZAR EMPLEADO
# ----------------------------------------------------------
@solo_admin
def actualizarEmpleado(request, IdEmpleado):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

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

    try:
        res = requests.put(f"{API_URL}{IdEmpleado}/", json=data, headers=headers)
        if res.status_code in (200, 202):
            return redirect('admin-crud-empleado')
        errores = res.json()
    except Exception as e:
        print("ERROR ACTUALIZANDO EMPLEADO:", e)
        errores = {"general": ["No se pudo conectar con la API"]}

    return render(request, 'templateCrudEmpleado/registro-empleado.html', {"data": data, "errores": errores})


# ----------------------------------------------------------
# DETALLE DE EMPLEADO
# ----------------------------------------------------------
@solo_admin
def detalleEmpleado(request, IdEmpleado):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        res = requests.get(f"{API_URL}{IdEmpleado}/", headers=headers)
        if res.status_code != 200:
            return redirect('admin-crud-empleado')
        empleado = res.json()
    except Exception as e:
        print("ERROR DETALLE EMPLEADO:", e)
        return redirect('admin-crud-empleado')

    return render(request, 'templateCrudEmpleado/detalle-empleado.html', {"emp": empleado})


# ----------------------------------------------------------
# CONFIRMAR ELIMINACIÓN
# ----------------------------------------------------------
@solo_admin
def confirmarEliminar(request, IdEmpleado):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    res = requests.get(f"{API_URL}{IdEmpleado}/", headers=headers)
    empleado = res.json() if res.status_code == 200 else None

    return render(request, 'templateCrudEmpleado/confirmar-eliminar.html', {"emp": empleado})


# ----------------------------------------------------------
# ELIMINAR EMPLEADO
# ----------------------------------------------------------
@solo_admin
def eliminarEmpleado(request, IdEmpleado):
    if request.method != "POST":
        return redirect('admin-crud-empleado')

    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    requests.delete(f"{API_URL}{IdEmpleado}/", headers=headers)
    return redirect('admin-crud-empleado')
