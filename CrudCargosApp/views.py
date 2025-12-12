import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from LoginApp.decorators import solo_admin

API_URL = "http://127.0.0.1:8000/cargos/"  # Cambia según tu API


# ----------------------------------------------------------
# FUNCIÓN PARA OBTENER HEADERS CON TOKEN
# ----------------------------------------------------------
def get_headers(request):
    token = request.session.get("token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


# ----------------------------------------------------------
# LISTAR TODOS LOS CARGOS
# ----------------------------------------------------------
@solo_admin
def cargosData(request):
    try:
        headers = get_headers(request)
        response = requests.get(API_URL, headers=headers)

        if response.status_code == 401:
            messages.error(request, "No autorizado. Debes iniciar sesión nuevamente.")
            return redirect("Login")

        cargos = response.json()
    except Exception as e:
        print("ERROR LISTANDO CARGOS:", e)
        cargos = []
        messages.error(request, "No se pudo conectar con la API.")

    return render(request, 'templateCrudCargo/cargos-models.html', {"Cargos": cargos})


# ----------------------------------------------------------
# REGISTRAR NUEVO CARGO
# ----------------------------------------------------------
@solo_admin
def cargosRegistracionView(request):

    # GET → Mostrar formulario vacío
    if request.method == "GET":
        return render(request, 'templateCrudCargo/registro-cargo.html', {"data": {}, "errores": {}})

    # POST → Enviar datos a la API
    data = {
        "TipoDeCargo": request.POST.get("TipoDeCargo"),
        "EstadoDelCargo": request.POST.get("EstadoDelCargo"),
        "DescripcionDelCargo": request.POST.get("DescripcionDelCargo"),
        "SueldoBase": request.POST.get("SueldoBase"),
    }

    headers = get_headers(request)
    res = requests.post(API_URL, json=data, headers=headers)

    if res.status_code == 201:
        messages.success(request, "Cargo registrado correctamente")
        return redirect("admin-crud-cargo")

    # Manejo de errores
    try:
        errores = res.json()
    except:
        errores = {"general": ["Error desconocido"]}

    return render(request, 'templateCrudCargo/registro-cargo.html', {"data": data, "errores": errores})


# ----------------------------------------------------------
# ACTUALIZAR CARGO EXISTENTE
# ----------------------------------------------------------
@solo_admin
def actualizarCargo(request, IdCargos):
    headers = get_headers(request)

    # GET → Obtener datos actuales
    if request.method == "GET":
        response = requests.get(f"{API_URL}{IdCargos}/", headers=headers)
        if response.status_code == 200:
            cargo = response.json()
        else:
            messages.error(request, "No se pudo obtener el cargo desde la API.")
            return redirect("admin-crud-cargo")

        return render(request, 'templateCrudCargo/registro-cargo.html', {"data": cargo, "errores": {}})

    # POST → Enviar datos actualizados
    data = {
        "TipoDeCargo": request.POST.get("TipoDeCargo"),
        "EstadoDelCargo": request.POST.get("EstadoDelCargo"),
        "DescripcionDelCargo": request.POST.get("DescripcionDelCargo"),
        "SueldoBase": request.POST.get("SueldoBase"),
    }

    res = requests.put(f"{API_URL}{IdCargos}/", json=data, headers=headers)

    if res.status_code in (200, 202):
        messages.success(request, "Cargo actualizado correctamente")
        return redirect("admin-crud-cargo")

    # Manejo de errores
    try:
        errores = res.json()
    except:
        errores = {"general": ["Error desconocido"]}

    return render(request, 'templateCrudCargo/registro-cargo.html', {"data": data, "errores": errores})


# ----------------------------------------------------------
# DETALLE DE CARGO
# ----------------------------------------------------------
@solo_admin
def detalleCargo(request, IdCargos):
    headers = get_headers(request)
    try:
        response = requests.get(f"{API_URL}{IdCargos}/", headers=headers)
        if response.status_code == 404:
            messages.error(request, "El cargo no existe.")
            return redirect("admin-crud-cargo")
        cargo = response.json()
    except Exception as e:
        print("ERROR DETALLE CARGO:", e)
        messages.error(request, "No se pudo obtener la información desde la API.")
        return redirect("admin-crud-cargo")

    return render(request, 'templateCrudCargo/detalle-cargo.html', {"cag": cargo})


# ----------------------------------------------------------
# CONFIRMAR ELIMINACIÓN
# ----------------------------------------------------------
@solo_admin
def confirmarEliminar(request, IdCargos):
    headers = get_headers(request)
    response = requests.get(f"{API_URL}{IdCargos}/", headers=headers)

    if response.status_code == 200:
        cargo = response.json()
    else:
        cargo = None

    return render(request, 'templateCrudCargo/confirmar-eliminar.html', {"cag": cargo})


# ----------------------------------------------------------
# ELIMINAR CARGO
# ----------------------------------------------------------
@solo_admin
def eliminarCargo(request, IdCargos):
    if request.method != "POST":
        messages.error(request, "Método no permitido para eliminar cargos.")
        return redirect("admin-crud-cargo")

    headers = get_headers(request)
    res = requests.delete(f"{API_URL}{IdCargos}/", headers=headers)

    if res.status_code in (200, 204):
        messages.success(request, "Cargo eliminado correctamente")
        try:
            cargo = res.json()
        except:
            pass
    else:
        messages.error(request, f"No se pudo eliminar: {res.text}")

    return redirect("admin-crud-cargo")
