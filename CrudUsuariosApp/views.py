import requests
from django.shortcuts import render, redirect
from django.contrib import messages
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
    token = request.session.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}

# ----------------------------
# LISTAR USUARIOS
# ----------------------------
@solo_admin
def usuariosData(request):
    try:
        res = requests.get(API_URL_USUARIOS, headers=get_headers(request))
        usuarios = res.json() if res.status_code == 200 else []
    except:
        usuarios = []
        messages.error(request, "No se pudo conectar con la API.")
    return render(request, 'templateCrudUsuario/usuarios-models.html', {"Usuarios": usuarios})

# ----------------------------
# REGISTRAR USUARIO
# ----------------------------
@solo_admin
def usuariosRegistrationView(request):
    try:
        Empleados = requests.get(API_URL_EMPLEADOS, headers=get_headers(request)).json()
        Cargos = requests.get(API_URL_CARGOS, headers=get_headers(request)).json()
        SuperUsuarios = requests.get(API_URL_AUTHUSER, headers=get_headers(request)).json()
        
        print("=== DEBUG EMPLEADOS ===")
        print(Empleados[0] if Empleados else "vacío")
        print("\n=== DEBUG CARGOS ===")
        print(Cargos[0] if Cargos else "vacío")
    except Exception as e:
        print(f"Error: {e}")
        Empleados, Cargos, SuperUsuarios = [], [], []
        messages.error(request, "No se pudieron cargar empleados, cargos o usuarios.")

    data, errores = {}, {}

    if request.method == "POST":
        data = {
            "Username": request.POST.get("Username", "").strip(),
            "Password": request.POST.get("Password", "").strip(),
            "ConfirmarPassword": request.POST.get("ConfirmarPassword", "").strip(),
            "CorreoElectronico": request.POST.get("CorreoElectronico", "").strip(),
        }

        try:
            data["Empleado"] = int(request.POST.get("Empleado"))
        except (ValueError, TypeError):
            data["Empleado"] = None

        try:
            data["Cargo"] = int(request.POST.get("Cargo"))
        except (ValueError, TypeError):
            data["Cargo"] = None

        try:
            data["SuperUserAsociado"] = int(request.POST.get("SuperUserAsociado")) if request.POST.get("SuperUserAsociado") else None
        except (ValueError, TypeError):
            data["SuperUserAsociado"] = None

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
                print("=== PAYLOAD ENVIADO ===")
                print(payload)
                res = requests.post(API_URL_USUARIOS, json=payload, headers=get_headers(request))
                print(f"=== STATUS CODE: {res.status_code} ===")
                print(f"=== RESPONSE: {res.text} ===")
                if res.status_code == 201:
                    messages.success(request, "Usuario registrado correctamente")
                    return redirect('admin-crud-usuario')
                errores.update(res.json())
            except Exception as e:
                print(f"=== EXCEPTION: {e} ===")
                errores["general"] = ["Error al conectar con la API"]

    return render(request, 'templateCrudUsuario/registro-usuario.html',
                  {"data": data, "errores": errores, "Empleados": Empleados, "Cargos": Cargos, "SuperUsuarios": SuperUsuarios})

# ----------------------------
# ACTUALIZAR USUARIO
# ----------------------------
@solo_admin
def actualizarUsuario(request, IdUsuarios):
    errores = {}
    data = {}

    # ----------------------------
    # CARGAR DATOS (GET)
    # ----------------------------
    if request.method == "GET":
        try:
            res = requests.get(
                f"{API_URL_USUARIOS}{IdUsuarios}/",
                headers=get_headers(request)
            )

            if res.status_code != 200:
                messages.error(request, "No se pudo cargar el usuario.")
                return redirect("admin-crud-usuario")

            usuario = res.json()

            data = {
                "Username": usuario.get("Username"),
                "CorreoElectronico": usuario.get("CorreoElectronico"),
            }

        except Exception as e:
            print(e)
            messages.error(request, "Error al conectar con la API.")
            return redirect("admin-crud-usuario")

        return render(
            request,
            "templateCrudUsuario/actualizar-usuario.html",
            {"data": data, "errores": errores}
        )

    # ----------------------------
    # PROCESAR EDICIÓN (POST)
    # ----------------------------
    data["Username"] = request.POST.get("Username", "")
    correo = request.POST.get("CorreoElectronico", "").strip()
    password = request.POST.get("Password", "").strip()
    confirmar = request.POST.get("ConfirmarPassword", "").strip()

    # ----------------------------
    # VALIDACIONES
    # ----------------------------
    if not correo:
        errores["CorreoElectronico"] = ["El correo es obligatorio"]

    if password or confirmar:
        if password != confirmar:
            errores["ConfirmarPassword"] = ["Las contraseñas no coinciden"]

    if errores:
        return render(
            request,
            "templateCrudUsuario/actualizar-usuario.html",
            {
                "data": {
                    "Username": data["Username"],
                    "CorreoElectronico": correo
                },
                "errores": errores
            }
        )

    # ----------------------------
    # PAYLOAD (solo editable)
    # ----------------------------
    payload = {
        "CorreoElectronico": correo
    }

    if password:
        payload["Password"] = password

    try:
        print("=== PAYLOAD EDICIÓN ===")
        print(payload)

        res = requests.patch(
            f"{API_URL_USUARIOS}{IdUsuarios}/",
            json=payload,
            headers=get_headers(request)
        )

        print(f"STATUS: {res.status_code}")
        print(f"RESPONSE: {res.text}")

        if res.status_code in (200, 202):
            messages.success(request, "Usuario actualizado correctamente")
            return redirect("admin-crud-usuario")

        errores.update(res.json())

    except Exception as e:
        print(e)
        errores["general"] = ["Error al conectar con la API"]

    return render(
        request,
        "templateCrudUsuario/actualizar-usuario.html",
        {
            "data": {
                "Username": data["Username"],
                "CorreoElectronico": correo
            },
            "errores": errores
        }
    )

# ----------------------------
# DETALLE USUARIO
# ----------------------------
@solo_admin
def detalleUsuario(request, IdUsuarios):
    headers = get_headers(request)
    usuario = {}
    Empleados, Cargos, SuperUsuarios = [], [], []

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
        messages.error(request, "No se pudo obtener la información desde la API.")

    return render(request, 'templateCrudUsuario/detalle-usuario.html', 
                  {"usu": usuario, "Empleados": Empleados, "Cargos": Cargos, "SuperUsuarios": SuperUsuarios})

# ----------------------------
# CONFIRMAR ELIMINACIÓN
# ----------------------------
@solo_admin
def confirmarEliminar(request, IdUsuarios):
    try:
        res = requests.get(f"{API_URL_USUARIOS}{IdUsuarios}/", headers=get_headers(request))
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
        messages.error(request, "Método no permitido para eliminar usuarios.")
        return redirect('admin-crud-usuario')

    try:
        res = requests.delete(f"{API_URL_USUARIOS}{IdUsuarios}/", headers=get_headers(request))
        if res.status_code in (200, 204):
            messages.success(request, "Usuario eliminado correctamente")
        else:
            messages.error(request, f"No se pudo eliminar: {res.text}")
    except:
        messages.error(request, "Error al conectar con la API")

    return redirect('admin-crud-usuario')