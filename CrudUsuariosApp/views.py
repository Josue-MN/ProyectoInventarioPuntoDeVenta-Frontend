import requests
from django.shortcuts import render, redirect
from LoginApp.decorators import solo_admin

# ----------------------------
# API URLs
# ----------------------------
API_URL_USUARIOS = "http://127.0.0.1:8000/usuarios/"
API_URL_EMPLEADOS = "http://127.0.0.1:8000/empleados/"
API_URL_CARGOS = "http://127.0.0.1:8000/cargos/"
API_URL_AUTHUSER = "http://127.0.0.1:8000/authuser/"

# ----------------------------
# Función auxiliar headers
# ----------------------------
def get_headers(request):
    token = request.COOKIES.get("token")
    if not token:
        return None
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

# ----------------------------
# LISTAR USUARIOS
# ----------------------------
@solo_admin
def usuariosData(request):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        res = requests.get(API_URL_USUARIOS, headers=headers)
        usuarios = res.json() if res.status_code == 200 else []
    except:
        usuarios = []

    return render(request, 'templateCrudUsuario/usuarios-models.html', {"Usuarios": usuarios})

# ----------------------------
# REGISTRAR USUARIO
# ----------------------------
@solo_admin
def usuariosRegistrationView(request):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        Empleados = requests.get(API_URL_EMPLEADOS, headers=headers).json()
        Cargos = requests.get(API_URL_CARGOS, headers=headers).json()
        SuperUsuarios = requests.get(API_URL_AUTHUSER, headers=headers).json()
    except:
        Empleados, Cargos, SuperUsuarios = [], [], []

    data, errores = {}, {}

    if request.method == "POST":
        data = {
            "Username": request.POST.get("Username", "").strip(),
            "Password": request.POST.get("Password", "").strip(),
            "ConfirmarPassword": request.POST.get("ConfirmarPassword", "").strip(),
            "CorreoElectronico": request.POST.get("CorreoElectronico", "").strip(),
        }

        for campo in ["Empleado", "Cargo", "SuperUserAsociado"]:
            try:
                data[campo] = int(request.POST.get(campo)) if request.POST.get(campo) else None
            except (ValueError, TypeError):
                data[campo] = None

        for campo in ["Username", "Password", "ConfirmarPassword", "CorreoElectronico", "Empleado", "Cargo"]:
            if not data.get(campo):
                errores[campo] = [f"El campo {campo} es obligatorio"]

        if data.get("Password") != data.get("ConfirmarPassword"):
            errores["ConfirmarPassword"] = ["Las contraseñas no coinciden"]

        if not errores:
            try:
                payload = {
                    "Username": data["Username"],
                    "Password": data["Password"],
                    "CorreoElectronico": data["CorreoElectronico"],
                    "Empleado": data["Empleado"],
                    "Cargo": data["Cargo"],
                    "UserAuth": data["SuperUserAsociado"],
                }
                res = requests.post(API_URL_USUARIOS, json=payload, headers=headers)
                if res.status_code == 201:
                    return redirect('admin-crud-usuario')
                errores.update(res.json())
            except:
                errores["general"] = ["Error al conectar con la API"]

    return render(request, 'templateCrudUsuario/registro-usuario.html',
                  {"data": data, "errores": errores, "Empleados": Empleados, "Cargos": Cargos, "SuperUsuarios": SuperUsuarios})

# ----------------------------
# ACTUALIZAR USUARIO
# ----------------------------
@solo_admin
def actualizarUsuario(request, IdUsuarios):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    errores = {}
    data = {}

    if request.method == "GET":
        try:
            res = requests.get(f"{API_URL_USUARIOS}{IdUsuarios}/", headers=headers)
            usuario = res.json() if res.status_code == 200 else {}
            data = {
                "Username": usuario.get("Username"),
                "CorreoElectronico": usuario.get("CorreoElectronico"),
            }
        except:
            data = {}
        return render(request, "templateCrudUsuario/actualizar-usuario.html",
                      {"data": data, "errores": errores})

    # POST → procesar edición
    data["Username"] = request.POST.get("Username", "")
    correo = request.POST.get("CorreoElectronico", "").strip()
    password = request.POST.get("Password", "").strip()
    confirmar = request.POST.get("ConfirmarPassword", "").strip()

    if password or confirmar:
        if password != confirmar:
            errores["ConfirmarPassword"] = ["Las contraseñas no coinciden"]

    if errores:
        return render(request, "templateCrudUsuario/actualizar-usuario.html",
                      {"data": {"Username": data["Username"], "CorreoElectronico": correo}, "errores": errores})

    payload = {"CorreoElectronico": correo}
    if password:
        payload["Password"] = password

    try:
        res = requests.patch(f"{API_URL_USUARIOS}{IdUsuarios}/", json=payload, headers=headers)
        if res.status_code in (200, 202):
            return redirect("admin-crud-usuario")
        errores.update(res.json())
    except:
        errores["general"] = ["Error al conectar con la API"]

    return render(request, "templateCrudUsuario/actualizar-usuario.html",
                  {"data": {"Username": data["Username"], "CorreoElectronico": correo}, "errores": errores})

# ----------------------------
# DETALLE USUARIO
# ----------------------------
@solo_admin
def detalleUsuario(request, IdUsuarios):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        res_usu = requests.get(f"{API_URL_USUARIOS}{IdUsuarios}/", headers=headers)
        usuario = res_usu.json() if res_usu.status_code == 200 else {}

        res_emp = requests.get(API_URL_EMPLEADOS, headers=headers)
        Empleados = res_emp.json() if res_emp.status_code == 200 else []

        res_car = requests.get(API_URL_CARGOS, headers=headers)
        Cargos = res_car.json() if res_car.status_code == 200 else []

        res_su = requests.get(API_URL_AUTHUSER, headers=headers)
        SuperUsuarios = res_su.json() if res_su.status_code == 200 else []
    except:
        usuario, Empleados, Cargos, SuperUsuarios = {}, [], [], []

    return render(request, 'templateCrudUsuario/detalle-usuario.html',
                  {"usu": usuario, "Empleados": Empleados, "Cargos": Cargos, "SuperUsuarios": SuperUsuarios})

# ----------------------------
# CONFIRMAR ELIMINACIÓN
# ----------------------------
@solo_admin
def confirmarEliminar(request, IdUsuarios):
    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        res = requests.get(f"{API_URL_USUARIOS}{IdUsuarios}/", headers=headers)
        usuario = res.json() if res.status_code == 200 else None
    except:
        usuario = None
    return render(request, 'templateCrudUsuario/confirmar-eliminar.html', {"usu": usuario})

# ----------------------------
# ELIMINAR USUARIO
# ----------------------------
@solo_admin
def eliminarUsuario(request, IdUsuarios):
    if request.method != "POST":
        return redirect('admin-crud-usuario')

    headers = get_headers(request)
    if not headers:
        return redirect("Login")

    try:
        requests.delete(f"{API_URL_USUARIOS}{IdUsuarios}/", headers=headers)
    except:
        pass

    return redirect('admin-crud-usuario')
