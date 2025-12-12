# Importa la función render (aunque en esta función no se usa directamente,
# normalmente está en views porque otras vistas sí la usan para devolver templates)
from django.shortcuts import render
# Importa el modelo AuditoriaBodega, que representa la tabla donde se guardan
# los registros de auditoría (qué pasó, en qué bodega, quién lo hizo, cuándo, etc.).
# Importa el modelo Usuarios para poder buscar al usuario logueado en la base de datos.
# Importa el decorador "solo_admin" desde la aplicación LoginApp.
# Este decorador sirve para restringir el acceso a ciertas vistas,
# permitiendole solo el ingreso de usuarios que tengan rol de administrador.
from LoginApp.decorators import solo_admin


def RegistrarAuditoriaBodega(request, bodega, accion):
    
    # Función de utilidad para registrar una auditoría asociada a una bodega.

    # Parámetros:
    #     request → el objeto HttpRequest que trae la sesión del usuario.
    #     bodega  → instancia del modelo Bodegas (objeto ya guardado en BD).
    #     accion  → string que indica la acción realizada ("CREAR", "ACTUALIZAR", "ELIMINAR", etc.).


    username = request.session.get("Usuario_Username")
    # Obtiene el nombre de usuario que guardaste en la sesión al momento del login.
    # Si no existe esa clave en la sesión, 'username' será None.

    usuario = None
    # Inicializa la variable 'usuario' en None por defecto. Esto sirve como
    # valor de respaldo en caso de que no se encuentre un usuario logueado
    # o no exista en la base de datos.

    if username:
        # Si en la sesión sí había un nombre de usuario (no es None, ni cadena vacía):

        usuario = Usuarios.objects.filter(Username=username).first()
        # Se hace una consulta sobre el modelo Usuarios filtrando por Username.
        # 'filter()' devuelve un queryset (lista de posibles usuarios).
        # 'first()' toma el primer resultado o devuelve None si no encontró nada.
        # Resultado:
        #   - Si existe un usuario con ese Username → usuario = instancia de Usuarios
        #   - Si no existe → usuario = None

    AuditoriaBodega.objects.create(
        Bodega=bodega,
        Usuario=usuario,
        BodegaIdRespaldo=bodega.IdBodega,
        BodegaNombreRespaldo=bodega.NombreBodega,
        Accion=accion
    )
    # Crea un nuevo registro en la tabla AuditoriaBodega.
    #
    # - Bodega=bodega
    #     Aquí se pasa el OBJETO completo de Bodegas. Django ORM automáticamente
    #     toma bodega.pk (IdBodega) y lo guarda en la columna FK 'BodegaId'.
    #
    # - Usuario=usuario
    #     Se pasa el OBJETO de Usuarios (o None). Si es un objeto válido, Django
    #     guarda usuario.pk (IdUsuarios) en la columna 'UsuarioId'.
    #     Si es None, la FK se guarda como NULL (permitido porque pusiste null=True).
    #
    # - Accion=accion
    #     Se guarda el string que indica qué se hizo (por ejemplo "REGISTRAR").
    #
    # Además, como en el modelo definiste:
    #     Fecha_hora = models.DateTimeField(auto_now_add=True)
    # Django automáticamente rellena ese campo con la fecha y hora actual
    # en el momento de crear este registro.

#---------------------------------------------------------------------------#

def RegistrarAuditoriaCargo(request, cargo, accion):
    
    username = request.session.get("Usuario_Username")
    usuario = None

    if username:
        usuario = Usuarios.objects.filter(Username=username).first()

    AuditoriaCargo.objects.create(
        Cargo=cargo,
        Usuario=usuario,
        CargoIdRespaldo=cargo.IdCargos,
        CargoNombreRespaldo=cargo.TipoDeCargo,
        Accion=accion
    )
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#

def RegistrarAuditoriaCategoria(request, categoria, accion):
    
    username = request.session.get("Usuario_Username")
    usuario = None

    if username:
        usuario = Usuarios.objects.filter(Username=username).first()

    AuditoriaCategoria.objects.create(
        Categoria=categoria,
        Usuario=usuario,
        CategoriaIdRespaldo=categoria.IdCategoriaProducto,
        CategoriaNombreRespaldo=categoria.NombreCategoria,
        Accion=accion
    )
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#

def RegistrarAuditoriaEmpleado(request, empleado, accion):
    
    username = request.session.get("Usuario_Username")
    usuario = None

    if username:
        usuario = Usuarios.objects.filter(Username=username).first()

    AuditoriaEmpleado.objects.create(
        Empleado=empleado,
        Usuario=usuario,
        EmpleadoIdRespaldo=empleado.IdEmpleado,
        EmpleadoNombreRespaldo=empleado.NombreEmpleado,
        Accion=accion
    )
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#

def RegistrarAuditoriaProducto(request, producto, accion):
    
    username = request.session.get("Usuario_Username")
    usuario = None

    if username:
        usuario = Usuarios.objects.filter(Username=username).first()

    AuditoriaProducto.objects.create(
        Producto=producto,
        Usuario=usuario,
        ProductoIdRespaldo=producto.IdProducto,
        ProductoNombreRespaldo=producto.NombreProducto,
        Accion=accion
    )
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#

def RegistrarAuditoriaUsuario(request, usuario, accion):

    username = request.session.get("Usuario_Username")
    usuarioSesion = None

    if username:
        usuarioSesion = Usuarios.objects.filter(Username=username).first()

    AuditoriaUsuario.objects.create(
        Usuario=usuarioSesion,
        UsuarioIdRespaldo=usuario.IdUsuarios,
        UsuarioNombreRespaldo=usuario.Username,
        Accion=accion
    )
#---------------------------------------------------------------------------#

@solo_admin
def AuditoriaData(request):
    auditoriaBodega = AuditoriaBodega.objects.all()
    auditoriaCargo = AuditoriaCargo.objects.all()
    auditoriaCategoria = AuditoriaCategoria.objects.all()
    auditoriaEmpleado = AuditoriaEmpleado.objects.all()
    auditoriaProducto = AuditoriaProducto.objects.all()
    auditoriaUsuario = AuditoriaUsuario.objects.all()

    data = {
        'AuditoriaBodega': auditoriaBodega,
        'AuditoriaCargo': auditoriaCargo,
        'AuditoriaCategoria': auditoriaCategoria,
        'AuditoriaEmpleado': auditoriaEmpleado,
        'AuditoriaProducto': auditoriaProducto,
        'AuditoriaUsuario': auditoriaUsuario,
    }

    return render(request, 'templateAuditoria/auditorias-mostrar.html', data)