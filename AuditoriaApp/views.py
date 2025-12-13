import requests
from django.shortcuts import render
from django.contrib import messages
from LoginApp.decorators import solo_admin

API_AUDITORIA_BODEGA = "http://127.0.0.1:8000/auditoriaBodega/"
API_AUDITORIA_CARGO = "http://127.0.0.1:8000/auditoriaCargo/"
API_AUDITORIA_CATEGORIA = "http://127.0.0.1:8000/auditoriaCategoria/"
API_AUDITORIA_EMPLEADO = "http://127.0.0.1:8000/auditoriaEmpleados/"
API_AUDITORIA_PRODUCTO = "http://127.0.0.1:8000/auditoriaProducto/"
API_AUDITORIA_USUARIO = "http://127.0.0.1:8000/auditoriaUsuario/"


def get_headers(request):
    token = request.COOKIES.get("token")
    if not token:
        return {}
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


@solo_admin
def AuditoriaData(request):
    try:
        auditoriaBodega = requests.get(API_AUDITORIA_BODEGA, headers=get_headers(request)).json()
        auditoriaCargo = requests.get(API_AUDITORIA_CARGO, headers=get_headers(request)).json()
        auditoriaCategoria = requests.get(API_AUDITORIA_CATEGORIA, headers=get_headers(request)).json()
        auditoriaEmpleado = requests.get(API_AUDITORIA_EMPLEADO, headers=get_headers(request)).json()
        auditoriaProducto = requests.get(API_AUDITORIA_PRODUCTO, headers=get_headers(request)).json()
        auditoriaUsuario = requests.get(API_AUDITORIA_USUARIO, headers=get_headers(request)).json()

    except Exception as e:
        print(e)
        messages.error(request, "Error al obtener las auditorías desde la API.")

        auditoriaBodega = []
        auditoriaCargo = []
        auditoriaCategoria = []
        auditoriaEmpleado = []
        auditoriaProducto = []
        auditoriaUsuario = []

    data = {
        'AuditoriaBodega': auditoriaBodega,
        'AuditoriaCargo': auditoriaCargo,
        'AuditoriaCategoria': auditoriaCategoria,
        'AuditoriaEmpleado': auditoriaEmpleado,
        'AuditoriaProducto': auditoriaProducto,
        'AuditoriaUsuario': auditoriaUsuario,
    }

    return render(
        request,
        'templateAuditoria/auditorias-mostrar.html',
        data
    )
