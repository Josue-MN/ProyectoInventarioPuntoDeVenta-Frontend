import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from LoginApp.decorators import login_requerido

API_URL_PRODUCTOS = "http://127.0.0.1:8000/productos/"
API_URL_CATEGORIAS = "http://127.0.0.1:8000/categoriaProducto/"
API_URL_BODEGAS = "http://127.0.0.1:8000/bodegas/"

def get_headers(request):
    token = request.session.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}

# ----------------------------
# LISTAR PRODUCTOS
# ----------------------------
@login_requerido
def productosData(request):
    try:
        res = requests.get(API_URL_PRODUCTOS, headers=get_headers(request))
        productos = res.json() if res.status_code == 200 else []
    except:
        productos = []
        messages.error(request, "No se pudo conectar con la API.")
    return render(request, 'templateCrudProducto/productos-models.html', {"Productos": productos})

# ----------------------------
# REGISTRAR NUEVO PRODUCTO
# ----------------------------
@login_requerido
def productosRegistrationView(request):
    try:
        Categorias = requests.get(API_URL_CATEGORIAS, headers=get_headers(request)).json()
        Bodegas = requests.get(API_URL_BODEGAS, headers=get_headers(request)).json()
    except:
        Categorias, Bodegas = [], []
        messages.error(request, "No se pudieron cargar categorías o bodegas.")

    data, errores = {}, {}

    if request.method == "POST":
        data = {
            "CodigoDeBarras": request.POST.get("CodigoDeBarras", "").strip(),
            "NombreProducto": request.POST.get("NombreProducto", "").strip(),
            "MarcaProducto": request.POST.get("MarcaProducto", "").strip(),
            "FechaDeVencimiento": request.POST.get("FechaDeVencimiento", "").strip(),
        }

        for campo in ["ValorProducto", "StockProducto", "CategoriaProducto", "Bodegas"]:
            try:
                data[campo] = int(request.POST.get(campo))
            except (ValueError, TypeError):
                data[campo] = None

        for campo in ["CodigoDeBarras", "NombreProducto", "ValorProducto", "StockProducto",
                      "MarcaProducto", "FechaDeVencimiento", "CategoriaProducto", "Bodegas"]:
            if not data.get(campo):
                errores[campo] = [f"El campo {campo} es obligatorio"]

        if not errores:
            try:
                res = requests.post(API_URL_PRODUCTOS, json=data, headers=get_headers(request))
                if res.status_code == 201:
                    messages.success(request, "Producto registrado correctamente")
                    usuario = request.session.get("Usuario_Username")
                    return redirect('admin-crud-producto' if usuario == "Admin" else 'crud-producto')
                errores.update(res.json())
            except:
                errores["general"] = ["Error al conectar con la API"]

    return render(request, 'templateCrudProducto/registro-producto.html',
                  {"data": data, "errores": errores, "Categorias": Categorias, "Bodegas": Bodegas})

# ----------------------------
# ACTUALIZAR PRODUCTO
# ----------------------------
@login_requerido
def actualizarProducto(request, IdProducto):
    try:
        Categorias = requests.get(API_URL_CATEGORIAS, headers=get_headers(request)).json()
        Bodegas = requests.get(API_URL_BODEGAS, headers=get_headers(request)).json()
    except:
        Categorias, Bodegas = [], []
        messages.error(request, "No se pudieron cargar categorías o bodegas.")

    if request.method == "GET":
        try:
            res = requests.get(f"{API_URL_PRODUCTOS}{IdProducto}/", headers=get_headers(request))
            data = res.json() if res.status_code == 200 else {}
        except:
            data = {}
            messages.error(request, "No se pudo cargar el producto.")
        return render(request, 'templateCrudProducto/registro-producto.html',
                      {"data": data, "errores": {}, "Categorias": Categorias, "Bodegas": Bodegas})

    data = {
        "CodigoDeBarras": request.POST.get("CodigoDeBarras", "").strip(),
        "NombreProducto": request.POST.get("NombreProducto", "").strip(),
        "MarcaProducto": request.POST.get("MarcaProducto", "").strip(),
        "FechaDeVencimiento": request.POST.get("FechaDeVencimiento", "").strip(),
    }

    for campo in ["ValorProducto", "StockProducto", "CategoriaProducto", "Bodegas"]:
        try:
            data[campo] = int(request.POST.get(campo))
        except (ValueError, TypeError):
            data[campo] = None

    errores = {}
    for campo in ["CodigoDeBarras", "NombreProducto", "ValorProducto", "StockProducto",
                  "MarcaProducto", "FechaDeVencimiento", "CategoriaProducto", "Bodegas"]:
        if not data.get(campo):
            errores[campo] = [f"El campo {campo} es obligatorio"]

    if not errores:
        try:
            res = requests.put(f"{API_URL_PRODUCTOS}{IdProducto}/", json=data, headers=get_headers(request))
            if res.status_code in (200, 202):
                messages.success(request, "Producto actualizado correctamente")
                usuario = request.session.get("Usuario_Username")
                return redirect('admin-crud-producto' if usuario == "Admin" else 'crud-producto')
            errores.update(res.json())
        except:
            errores["general"] = ["Error al conectar con la API"]

    return render(request, 'templateCrudProducto/registro-producto.html',
                  {"data": data, "errores": errores, "Categorias": Categorias, "Bodegas": Bodegas})

# ----------------------------
# DETALLE DEL PRODUCTO
# ----------------------------
@login_requerido
def detalleProducto(request, IdProducto):
    headers = get_headers(request)
    producto = {}
    Categorias, Bodegas = [], []

    try:
        res_pro = requests.get(f"{API_URL_PRODUCTOS}{IdProducto}/", headers=headers)
        producto = res_pro.json() if res_pro.status_code == 200 else {}

        res_cat = requests.get(API_URL_CATEGORIAS, headers=headers)
        Categorias = res_cat.json() if res_cat.status_code == 200 else []

        res_bod = requests.get(API_URL_BODEGAS, headers=headers)
        Bodegas = res_bod.json() if res_bod.status_code == 200 else []
    except Exception as e:
        messages.error(request, "No se pudo obtener la información desde la API.")

    return render(request, 'templateCrudProducto/detalle-producto.html', 
                  {"pro": producto, "Categorias": Categorias, "Bodegas": Bodegas})
# ----------------------------
# CONFIRMAR ELIMINACIÓN
# ----------------------------
@login_requerido
def confirmarEliminar(request, IdProducto):
    try:
        res = requests.get(f"{API_URL_PRODUCTOS}{IdProducto}/", headers=get_headers(request))
        producto = res.json() if res.status_code == 200 else None
    except:
        producto = None
    return render(request, 'templateCrudProducto/confirmar-eliminar.html', {"pro": producto})

# ----------------------------
# ELIMINAR PRODUCTO
# ----------------------------
@login_requerido
def eliminarProducto(request, IdProducto):
    if request.method != "POST":
        messages.error(request, "Método no permitido para eliminar productos.")
        usuario = request.session.get("Usuario_Username")
        return redirect('admin-crud-producto' if usuario == "Admin" else 'crud-producto')

    try:
        res = requests.delete(f"{API_URL_PRODUCTOS}{IdProducto}/", headers=get_headers(request))
        if res.status_code in (200, 204):
            messages.success(request, "Producto eliminado correctamente")
        else:
            messages.error(request, f"No se pudo eliminar: {res.text}")
    except:
        messages.error(request, "Error al conectar con la API")

    usuario = request.session.get("Usuario_Username")
    return redirect('admin-crud-producto' if usuario == "Admin" else 'crud-producto')
