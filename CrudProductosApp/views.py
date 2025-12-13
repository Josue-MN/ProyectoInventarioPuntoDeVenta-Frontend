import requests
from django.shortcuts import render, redirect
from LoginApp.decorators import login_requerido

API_URL_PRODUCTOS = "http://127.0.0.1:8000/productos/"
API_URL_CATEGORIAS = "http://127.0.0.1:8000/categoriaProducto/"
API_URL_BODEGAS = "http://127.0.0.1:8000/bodegas/"

def get_headers(request):
    token = request.COOKIES.get("token")
    if not token:
        return None
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

# ----------------------------
# LISTAR PRODUCTOS
# ----------------------------
@login_requerido
def productosData(request):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        res = requests.get(API_URL_PRODUCTOS, headers=headers)
        productos = res.json() if res.status_code == 200 else []
    except:
        productos = []

    return render(request, 'templateCrudProducto/productos-models.html', {"Productos": productos})

# ----------------------------
# REGISTRAR NUEVO PRODUCTO
# ----------------------------
@login_requerido
def productosRegistrationView(request):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        Categorias = requests.get(API_URL_CATEGORIAS, headers=headers).json()
        Bodegas = requests.get(API_URL_BODEGAS, headers=headers).json()
    except:
        Categorias, Bodegas = [], []

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
                res = requests.post(API_URL_PRODUCTOS, json=data, headers=headers)
                if res.status_code == 201:
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
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        Categorias = requests.get(API_URL_CATEGORIAS, headers=headers).json()
        Bodegas = requests.get(API_URL_BODEGAS, headers=headers).json()
    except:
        Categorias, Bodegas = [], []

    if request.method == "GET":
        try:
            res = requests.get(f"{API_URL_PRODUCTOS}{IdProducto}/", headers=headers)
            data = res.json() if res.status_code == 200 else {}
        except:
            data = {}
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
            res = requests.put(f"{API_URL_PRODUCTOS}{IdProducto}/", json=data, headers=headers)
            if res.status_code in (200, 202):
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
    if not headers:
        return redirect("Login")

    try:
        res_pro = requests.get(f"{API_URL_PRODUCTOS}{IdProducto}/", headers=headers)
        producto = res_pro.json() if res_pro.status_code == 200 else {}

        res_cat = requests.get(API_URL_CATEGORIAS, headers=headers)
        Categorias = res_cat.json() if res_cat.status_code == 200 else []

        res_bod = requests.get(API_URL_BODEGAS, headers=headers)
        Bodegas = res_bod.json() if res_bod.status_code == 200 else []
    except:
        producto, Categorias, Bodegas = {}, [], []

    return render(request, 'templateCrudProducto/detalle-producto.html',
                  {"pro": producto, "Categorias": Categorias, "Bodegas": Bodegas})

# ----------------------------
# CONFIRMAR ELIMINACIÓN
# ----------------------------
@login_requerido
def confirmarEliminar(request, IdProducto):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        res = requests.get(f"{API_URL_PRODUCTOS}{IdProducto}/", headers=headers)
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
        usuario = request.session.get("Usuario_Username")
        return redirect('admin-crud-producto' if usuario == "Admin" else 'crud-producto')

    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        requests.delete(f"{API_URL_PRODUCTOS}{IdProducto}/", headers=headers)
    except:
        pass

    usuario = request.session.get("Usuario_Username")
    return redirect('admin-crud-producto' if usuario == "Admin" else 'crud-producto')
