import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from LoginApp.decorators import login_requerido

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


# ----------------------------------------------------------
# LISTAR TODAS LAS BODEGAS
# ----------------------------------------------------------
@login_requerido
def bodegasData(request):
    try:
        headers = get_headers(request)
        response = requests.get(API_URL, headers=headers)

        if response.status_code == 401:
            messages.error(request, "No autorizado. Debes iniciar sesión nuevamente.")
            return redirect("Login")

        bodegas = response.json()

    except Exception as e:
        print("ERROR LISTANDO:", e)
        bodegas = []
        messages.error(request, "No se pudo conectar con la API.")

    return render(request, "templateCrudBodega/bodegas-models.html", {"Bodegas": bodegas})


# ----------------------------------------------------------
# REGISTRAR BODEGA
# ----------------------------------------------------------
@login_requerido
def bodegasRegistracionView(request):

    # GET → Mostrar el formulario vacío
    if request.method == "GET":
        return render(request, "templateCrudBodega/registro-bodega.html", {
            "errores": {},
            "data": {}
        })

    # POST → Enviar datos a la API
    if request.method == "POST":
        data = {
            "NombreBodega": request.POST.get("NombreBodega"),
            "UbicacionBodega": request.POST.get("UbicacionBodega"),
            "EstadoBodega": request.POST.get("EstadoBodega"),
            "ObservacionesBodega": request.POST.get("ObservacionesBodega"),
        }

        headers = get_headers(request)
        res = requests.post(API_URL, json=data, headers=headers)

        # Si se creó correctamente
        if res.status_code == 201:
            messages.success(request, "Bodega registrada correctamente")
            return redirect("crud-bodega")

        # Si hay errores de validación
        try:
            errores = res.json()
        except:
            errores = {"general": ["Error desconocido"]}

        return render(
            request,
            "templateCrudBodega/registro-bodega.html",
            {"errores": errores, "data": data}
        )



# ----------------------------------------------------------
# DETALLE
# ----------------------------------------------------------
@login_requerido
def detalleBodega(request, IdBodega):
    try:
        headers = get_headers(request)
        response = requests.get(f"{API_URL}{IdBodega}/", headers=headers)

        if response.status_code == 404:
            messages.error(request, "La bodega no existe.")
            return redirect("crud-bodega")

        bodega = response.json()

    except Exception as e:
        print("ERROR DETALLE:", e)
        bodega = None
        messages.error(request, "No se pudo obtener la información desde la API.")

    return render(request, "templateCrudBodega/detalle-bodega.html", {"bod": bodega})


# ----------------------------------------------------------
# ACTUALIZAR
# ----------------------------------------------------------
@login_requerido
def actualizarBodega(request, IdBodega):

    headers = get_headers(request)

    # Obtener datos actuales
    response = requests.get(f"{API_URL}{IdBodega}/", headers=headers)
    if response.status_code == 200:
        bodega = response.json()
    else:
        messages.error(request, "No se pudo obtener la bodega desde la API.")
        return redirect("crud-bodega")

    if request.method == "POST":
        data = {
            "NombreBodega": request.POST.get("NombreBodega"),
            "UbicacionBodega": request.POST.get("UbicacionBodega"),
            "EstadoBodega": request.POST.get("EstadoBodega"),
            "ObservacionesBodega": request.POST.get("ObservacionesBodega"),
        }

        res = requests.put(f"{API_URL}{IdBodega}/", json=data, headers=headers)

        if res.status_code in (200, 202):
            messages.success(request, "Bodega actualizada correctamente")
            return redirect("crud-bodega")
        else:
            messages.error(request, f"Error al actualizar la bodega: {res.text}")

    return render(request, "templateCrudBodega/registro-bodega.html", {"bodega": bodega})


# ----------------------------------------------------------
# CONFIRMAR ELIMINAR
# ----------------------------------------------------------
@login_requerido
def confirmarEliminar(request, IdBodega):

    headers = get_headers(request)
    response = requests.get(f"{API_URL}{IdBodega}/", headers=headers)

    if response.status_code == 200:
        bodega = response.json()
    else:
        bodega = None

    return render(request, "templateCrudBodega/confirmar-eliminar.html", {"bod": bodega})


# ----------------------------------------------------------
# ELIMINAR
# ----------------------------------------------------------
@login_requerido
def eliminarBodega(request, IdBodega):

    if request.method == "POST":

        headers = get_headers(request)
        res = requests.delete(f"{API_URL}{IdBodega}/", headers=headers)

        if res.status_code in (200, 204):
            messages.success(request, "Bodega eliminada correctamente")
        else:
            messages.error(request, f"No se pudo eliminar: {res.text}")

        return redirect("crud-bodega")

    messages.error(request, "Método no permitido.")
    return redirect("crud-bodega")
