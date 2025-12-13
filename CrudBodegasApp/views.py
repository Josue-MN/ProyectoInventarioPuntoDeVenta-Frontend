import requests
from django.shortcuts import render, redirect
from LoginApp.decorators import login_requerido

API_URL = "http://127.0.0.1:8000/bodegas/"


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
# LISTAR BODEGAS
# ----------------------------------------------------------
@login_requerido
def bodegasData(request):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        res = requests.get(API_URL, headers=headers)
        if res.status_code == 401:
            return redirect("Login")

        bodegas = res.json()
    except Exception as e:
        print("ERROR LISTANDO BODEGAS:", e)
        bodegas = []

    return render(
        request,
        "templateCrudBodega/bodegas-models.html",
        {"Bodegas": bodegas},
    )


# ----------------------------------------------------------
# REGISTRAR BODEGA
# ----------------------------------------------------------
@login_requerido
def bodegasRegistracionView(request):
    if request.method == "GET":
        return render(
            request,
            "templateCrudBodega/registro-bodega.html",
            {"errores": {}, "data": {}},
        )

    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    data = {
        "NombreBodega": request.POST.get("NombreBodega"),
        "UbicacionBodega": request.POST.get("UbicacionBodega"),
        "EstadoBodega": request.POST.get("EstadoBodega"),
        "ObservacionesBodega": request.POST.get("ObservacionesBodega"),
    }

    try:
        res = requests.post(API_URL, json=data, headers=headers)

        if res.status_code == 201:
            return redirect("crud-bodega")

        errores = res.json()
    except Exception as e:
        print("ERROR REGISTRANDO:", e)
        errores = {"general": ["No se pudo conectar con la API"]}

    return render(
        request,
        "templateCrudBodega/registro-bodega.html",
        {"errores": errores, "data": data},
    )


# ----------------------------------------------------------
# DETALLE
# ----------------------------------------------------------
@login_requerido
def detalleBodega(request, IdBodega):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        res = requests.get(f"{API_URL}{IdBodega}/", headers=headers)
        if res.status_code != 200:
            return redirect("crud-bodega")

        bodega = res.json()
    except Exception as e:
        print("ERROR DETALLE:", e)
        return redirect("crud-bodega")

    return render(
        request,
        "templateCrudBodega/detalle-bodega.html",
        {"bod": bodega},
    )


# ----------------------------------------------------------
# ACTUALIZAR
# ----------------------------------------------------------
@login_requerido
def actualizarBodega(request, IdBodega):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    if request.method == "GET":
        res = requests.get(f"{API_URL}{IdBodega}/", headers=headers)
        if res.status_code != 200:
            return redirect("crud-bodega")

        return render(
            request,
            "templateCrudBodega/registro-bodega.html",
            {"data": res.json(), "errores": {}},
        )

    data = {
        "NombreBodega": request.POST.get("NombreBodega"),
        "UbicacionBodega": request.POST.get("UbicacionBodega"),
        "EstadoBodega": request.POST.get("EstadoBodega"),
        "ObservacionesBodega": request.POST.get("ObservacionesBodega"),
    }

    try:
        res = requests.put(f"{API_URL}{IdBodega}/", json=data, headers=headers)

        if res.status_code in (200, 202):
            return redirect("crud-bodega")

        errores = res.json()
    except Exception as e:
        print("ERROR ACTUALIZANDO:", e)
        errores = {"general": ["No se pudo conectar con la API"]}

    return render(
        request,
        "templateCrudBodega/registro-bodega.html",
        {"data": data, "errores": errores},
    )


# ----------------------------------------------------------
# CONFIRMAR ELIMINAR
# ----------------------------------------------------------
@login_requerido
def confirmarEliminar(request, IdBodega):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    res = requests.get(f"{API_URL}{IdBodega}/", headers=headers)
    bodega = res.json() if res.status_code == 200 else None

    return render(
        request,
        "templateCrudBodega/confirmar-eliminar.html",
        {"bod": bodega},
    )


# ----------------------------------------------------------
# ELIMINAR
# ----------------------------------------------------------
@login_requerido
def eliminarBodega(request, IdBodega):
    if request.method != "POST":
        return redirect("crud-bodega")

    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    requests.delete(f"{API_URL}{IdBodega}/", headers=headers)
    return redirect("crud-bodega")
