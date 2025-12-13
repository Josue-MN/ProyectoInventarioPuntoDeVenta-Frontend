import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from LoginApp.decorators import login_requerido

API_URL = "http://127.0.0.1:8000/categoriaProducto/"  # Cambia según tu API

# ----------------------------------------------------------
# FUNCIONES AUXILIARES
# ----------------------------------------------------------
def get_headers(request):
    token = request.session.get("token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}

# ----------------------------------------------------------
# LISTAR CATEGORÍAS
# ----------------------------------------------------------
@login_requerido
def categoriaProductoData(request):
    try:
        headers = get_headers(request)
        response = requests.get(API_URL, headers=headers)

        if response.status_code == 401:
            messages.error(request, "No autorizado. Debes iniciar sesión nuevamente.")
            return redirect("Login")
        
        categorias = response.json()
    except Exception as e:
        print("ERROR LISTANDO CATEGORIAS:", e)
        categorias = []
        messages.error(request, "No se pudo conectar con la API.")

    return render(request, 'templateCrudCategoriaProducto/categoriaProducto-models.html', {"CategoriaProducto": categorias})

# ----------------------------------------------------------
# REGISTRAR NUEVA CATEGORÍA
# ----------------------------------------------------------
@login_requerido
def categoriaProductoRegistracionView(request):

    if request.method == "GET":
        return render(request, 'templateCrudCategoriaProducto/registro-categoriaProducto.html', {"data": {}, "errores": {}})

    # POST → enviar datos a la API
    data = {
        "NombreCategoria": request.POST.get("NombreCategoria"),
        "Descripcion": request.POST.get("Descripcion"),
        "Estado": request.POST.get("Estado"),
        "Observaciones": request.POST.get("Observaciones"),
    }

    headers = get_headers(request)
    res = requests.post(API_URL, json=data, headers=headers)

    if res.status_code == 201:
        messages.success(request, "Categoría registrada correctamente")
        usuario = request.session.get('Usuario_Username')
        return redirect('admin-crud-categoria')

    # Manejo de errores
    try:
        errores = res.json()
    except:
        errores = {"general": ["Error desconocido"]}
    return render(request, 'templateCrudCategoriaProducto/registro-categoriaProducto.html', {"data": data, "errores": errores})

# ----------------------------------------------------------
# ACTUALIZAR CATEGORÍA
# ----------------------------------------------------------
@login_requerido
def actualizarCategoriaProducto(request, IdCategoriaProducto):
    headers = get_headers(request)

    if request.method == "GET":
        res = requests.get(f"{API_URL}{IdCategoriaProducto}/", headers=headers)
        categoria = res.json() if res.status_code == 200 else {}
        return render(request, 'templateCrudCategoriaProducto/registro-categoriaProducto.html', {"data": categoria, "errores": {}})

    # POST → enviar actualización a la API
    data = {
        "NombreCategoria": request.POST.get("NombreCategoria"),
        "Descripcion": request.POST.get("Descripcion"),
        "Estado": request.POST.get("Estado"),
        "Observaciones": request.POST.get("Observaciones"),
    }

    res = requests.put(f"{API_URL}{IdCategoriaProducto}/", json=data, headers=headers)
    if res.status_code in (200, 202):
        messages.success(request, "Categoría actualizada correctamente")
        usuario = request.session.get('Usuario_Username')
        return redirect('admin-crud-categoria')

    # Manejo de errores
    try:
        errores = res.json()
    except:
        errores = {"general": ["Error desconocido"]}
    return render(request, 'templateCrudCategoriaProducto/registro-categoriaProducto.html', {"data": data, "errores": errores})

# ----------------------------------------------------------
# DETALLE DE CATEGORÍA
# ----------------------------------------------------------
@login_requerido
def detalleCategoriaProducto(request, IdCategoriaProducto):
    headers = get_headers(request)
    try:
        res = requests.get(f"{API_URL}{IdCategoriaProducto}/", headers=headers)
        categoria = res.json() if res.status_code == 200 else {}
    except Exception as e:
        print("ERROR DETALLE CATEGORIA:", e)
        messages.error(request, "No se pudo obtener la información desde la API.")
        return redirect("admin-crud-categoria")
    return render(request, 'templateCrudCategoriaProducto/detalle-categoriaProducto.html', {"bod": categoria})

# ----------------------------------------------------------
# CONFIRMAR ELIMINACIÓN
# ----------------------------------------------------------
@login_requerido
def confirmarEliminar(request, IdCategoriaProducto):
    headers = get_headers(request)
    res = requests.get(f"{API_URL}{IdCategoriaProducto}/", headers=headers)
    categoria = res.json() if res.status_code == 200 else None
    return render(request, 'templateCrudCategoriaProducto/confirmar-eliminar.html', {"bod": categoria})

# ----------------------------------------------------------
# ELIMINAR CATEGORÍA
# ----------------------------------------------------------
@login_requerido
def eliminarCategoriaProducto(request, IdCategoriaProducto):
    if request.method != "POST":
        messages.error(request, "Método no permitido para eliminar categorías.")
        return redirect("admin-crud-categoria")

    headers = get_headers(request)
    res = requests.delete(f"{API_URL}{IdCategoriaProducto}/", headers=headers)

    if res.status_code in (200, 204):
        messages.success(request, "Categoría eliminada correctamente")
    else:
        messages.error(request, f"No se pudo eliminar: {res.text}")

    usuario = request.session.get('Usuario_Username')
    return redirect('admin-crud-categoria')
