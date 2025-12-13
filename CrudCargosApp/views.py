import requests
from django.shortcuts import render, redirect
from LoginApp.decorators import solo_admin

API_URL = "http://127.0.0.1:8000/cargos/"  # Cambia según tu API


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
# LISTAR CARGOS
# ----------------------------------------------------------
@solo_admin
def cargosData(request):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        res = requests.get(API_URL, headers=headers)
        if res.status_code == 401:
            return redirect("Login")
        cargos = res.json()
    except Exception as e:
        print("ERROR LISTANDO CARGOS:", e)
        cargos = []

    return render(request, 'templateCrudCargo/cargos-models.html', {"Cargos": cargos})


# ----------------------------------------------------------
# REGISTRAR NUEVO CARGO
# ----------------------------------------------------------
@solo_admin
def cargosRegistracionView(request):
    if request.method == "GET":
        return render(request, 'templateCrudCargo/registro-cargo.html', {"data": {}, "errores": {}})

    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    data = {
        "TipoDeCargo": request.POST.get("TipoDeCargo"),
        "EstadoDelCargo": request.POST.get("EstadoDelCargo"),
        "DescripcionDelCargo": request.POST.get("DescripcionDelCargo"),
        "SueldoBase": request.POST.get("SueldoBase"),
    }

    try:
        res = requests.post(API_URL, json=data, headers=headers)
        if res.status_code == 201:
            return redirect("admin-crud-cargo")
        errores = res.json()
    except Exception as e:
        print("ERROR REGISTRANDO CARGO:", e)
        errores = {"general": ["No se pudo conectar con la API"]}

    return render(request, 'templateCrudCargo/registro-cargo.html', {"data": data, "errores": errores})


# ----------------------------------------------------------
# ACTUALIZAR CARGO
# ----------------------------------------------------------
@solo_admin
def actualizarCargo(request, IdCargos):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    if request.method == "GET":
        res = requests.get(f"{API_URL}{IdCargos}/", headers=headers)
        if res.status_code != 200:
            return redirect("admin-crud-cargo")
        return render(request, 'templateCrudCargo/registro-cargo.html', {"data": res.json(), "errores": {}})

    data = {
        "TipoDeCargo": request.POST.get("TipoDeCargo"),
        "EstadoDelCargo": request.POST.get("EstadoDelCargo"),
        "DescripcionDelCargo": request.POST.get("DescripcionDelCargo"),
        "SueldoBase": request.POST.get("SueldoBase"),
    }

    try:
        res = requests.put(f"{API_URL}{IdCargos}/", json=data, headers=headers)
        if res.status_code in (200, 202):
            return redirect("admin-crud-cargo")
        errores = res.json()
    except Exception as e:
        print("ERROR ACTUALIZANDO CARGO:", e)
        errores = {"general": ["No se pudo conectar con la API"]}

    return render(request, 'templateCrudCargo/registro-cargo.html', {"data": data, "errores": errores})


# ----------------------------------------------------------
# DETALLE DE CARGO
# ----------------------------------------------------------
@solo_admin
def detalleCargo(request, IdCargos):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        res = requests.get(f"{API_URL}{IdCargos}/", headers=headers)
        if res.status_code != 200:
            return redirect("admin-crud-cargo")
        cargo = res.json()
    except Exception as e:
        print("ERROR DETALLE CARGO:", e)
        return redirect("admin-crud-cargo")

    return render(request, 'templateCrudCargo/detalle-cargo.html', {"cag": cargo})


# ----------------------------------------------------------
# CONFIRMAR ELIMINACIÓN
# ----------------------------------------------------------
@solo_admin
def confirmarEliminar(request, IdCargos):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    res = requests.get(f"{API_URL}{IdCargos}/", headers=headers)
    cargo = res.json() if res.status_code == 200 else None

    return render(request, 'templateCrudCargo/confirmar-eliminar.html', {"cag": cargo})


# ----------------------------------------------------------
# ELIMINAR CARGO
# ----------------------------------------------------------
@solo_admin
def eliminarCargo(request, IdCargos):
    if request.method != "POST":
        return redirect("admin-crud-cargo")

    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    requests.delete(f"{API_URL}{IdCargos}/", headers=headers)
    return redirect("admin-crud-cargo")
