import requests
from django.shortcuts import render, redirect
from LoginApp.decorators import login_requerido

API_URL = "http://127.0.0.1:8000/categoriaProducto/"

# ----------------------------------------------------------
# HEADERS API
# ----------------------------------------------------------
def get_headers(request):
    token = request.COOKIES.get("token")
    if not token:
        return {}
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

# ----------------------------------------------------------
# LISTAR CATEGORÍAS
# ----------------------------------------------------------
@login_requerido
def categoriaProductoData(request):
    try:
        response = requests.get(API_URL, headers=get_headers(request), timeout=5)

        if response.status_code == 401:
            return redirect("Login")

        categorias = response.json()

    except Exception as e:
        print("ERROR LISTANDO CATEGORIAS:", e)
        categorias = []
        error = "No se pudo conectar con la API."
        return render(
            request,
            "templateCrudCategoriaProducto/categoriaProducto-models.html",
            {"CategoriaProducto": categorias, "error": error},
        )

    return render(
        request,
        "templateCrudCategoriaProducto/categoriaProducto-models.html",
        {"CategoriaProducto": categorias},
    )

# ----------------------------------------------------------
# REGISTRAR CATEGORÍA
# ----------------------------------------------------------
@login_requerido
def categoriaProductoRegistracionView(request):

    if request.method == "GET":
        return render(
            request,
            "templateCrudCategoriaProducto/registro-categoriaProducto.html",
            {"data": {}, "errores": {}},
        )

    data = {
        "NombreCategoria": request.POST.get("NombreCategoria"),
        "Descripcion": request.POST.get("Descripcion"),
        "Estado": request.POST.get("Estado"),
        "Observaciones": request.POST.get("Observaciones"),
    }

    res = requests.post(API_URL, json=data, headers=get_headers(request))

    if res.status_code == 201:
        return redirect("admin-crud-categoria")

    try:
        errores = res.json()
    except:
        errores = {"general": ["Error desconocido"]}

    return render(
        request,
        "templateCrudCategoriaProducto/registro-categoriaProducto.html",
        {"data": data, "errores": errores},
    )

# ----------------------------------------------------------
# ACTUALIZAR CATEGORÍA
# ----------------------------------------------------------
@login_requerido
def actualizarCategoriaProducto(request, IdCategoriaProducto):
    headers = get_headers(request)

    if request.method == "GET":
        res = requests.get(f"{API_URL}{IdCategoriaProducto}/", headers=headers)
        categoria = res.json() if res.status_code == 200 else {}
        return render(
            request,
            "templateCrudCategoriaProducto/registro-categoriaProducto.html",
            {"data": categoria, "errores": {}},
        )

    data = {
        "NombreCategoria": request.POST.get("NombreCategoria"),
        "Descripcion": request.POST.get("Descripcion"),
        "Estado": request.POST.get("Estado"),
        "Observaciones": request.POST.get("Observaciones"),
    }

    res = requests.put(f"{API_URL}{IdCategoriaProducto}/", json=data, headers=headers)

    if res.status_code in (200, 202):
        return redirect("admin-crud-categoria")

    try:
        errores = res.json()
    except:
        errores = {"general": ["Error desconocido"]}

    return render(
        request,
        "templateCrudCategoriaProducto/registro-categoriaProducto.html",
        {"data": data, "errores": errores},
    )

# ----------------------------------------------------------
# DETALLE CATEGORÍA
# ----------------------------------------------------------
@login_requerido
def detalleCategoriaProducto(request, IdCategoriaProducto):
    try:
        res = requests.get(
            f"{API_URL}{IdCategoriaProducto}/",
            headers=get_headers(request),
        )
        categoria = res.json() if res.status_code == 200 else {}
    except Exception as e:
        print("ERROR DETALLE CATEGORIA:", e)
        return redirect("admin-crud-categoria")

    return render(
        request,
        "templateCrudCategoriaProducto/detalle-categoriaProducto.html",
        {"bod": categoria},
    )

# ----------------------------------------------------------
# CONFIRMAR ELIMINACIÓN
# ----------------------------------------------------------
@login_requerido
def confirmarEliminar(request, IdCategoriaProducto):
    res = requests.get(
        f"{API_URL}{IdCategoriaProducto}/",
        headers=get_headers(request),
    )
    categoria = res.json() if res.status_code == 200 else None

    return render(
        request,
        "templateCrudCategoriaProducto/confirmar-eliminar.html",
        {"bod": categoria},
    )

# ----------------------------------------------------------
# ELIMINAR CATEGORÍA
# ----------------------------------------------------------
@login_requerido
def eliminarCategoriaProducto(request, IdCategoriaProducto):

    if request.method != "POST":
        return redirect("admin-crud-categoria")

    res = requests.delete(
        f"{API_URL}{IdCategoriaProducto}/",
        headers=get_headers(request),
    )

    return redirect("admin-crud-categoria")
