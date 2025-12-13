from django.urls import path, include
from AdminHomeApp.views import renderAdminHome  # Importa la view que renderiza el home del administrador
from CrudEmpleadosApp import views  # Importa views de la app CrudEmpleadosApp
from CrudUsuariosApp import views  # Importa views de la app CrudUsuariosApp
from CrudProductosApp import views  # Importa views de la app CrudProductosApp
from CrudCategoriaProductoApp import views  # Importa views de la app CrudCategoriasApp
from CrudBodegasApp import views  # Importa views de la app CrudBodegaApp
from CrudCargosApp import views  # Importa views de la app CrudBodegaApp

# Lista principal de rutas del proyecto
urlpatterns = [

    # Ruta principal del panel admin. Cuando se entra a "/" carga la vista renderAdminHome
    path('', renderAdminHome, name='adminhome'),

    # Incluye todas las rutas de la app CrudEmpleadosApp dentro del enrutador principal
    # Al usar "" como prefijo, estas rutas se cargan directamente desde la raíz sin prefijo
    path("", include("CrudEmpleadosApp.urls_admin")),

    # Incluye las rutas personalizadas para usuarios
    path("", include("CrudUsuariosApp.urls_admin")),

    # Incluye las rutas para la gestión de cargos
    path("", include("CrudCargosApp.urls_admin")),

    # Incluye las rutas del CRUD de productos
    path("", include("CrudProductosApp.urls_admin")),

    # Incluye las rutas del CRUD de bodegas
    path("", include("CrudBodegasApp.urls_admin")),

    # Incluye las rutas del CRUD de categorías de productos
    path("", include("CrudCategoriaProductoApp.urls_admin")),

    # Incluye las rutas del módulo de auditoría
    path("", include("AuditoriaApp.urls")),
]
