from django.contrib import admin
from CrudCategoriaProductoApp.models import CategoriaProducto
from CrudCategoriaProductoApp.forms import CategoriaProductoRegistracionForm

# Register your models here.
class CategoriaProductoAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista principal del admin
    list_display = [
        "IdCategoriaProducto",
        "NombreCategoria", 
        "Descripcion",
        "Estado",
        "Observaciones"]
    # Campos por los cuales se puede filtrar en la barra lateral
    list_filter = [
        "NombreCategoria",
        "Estado"]
    # Campos que se pueden buscar en la barra de búsqueda del admin
    search_fields = [
        "IdCategoriaProducto",
        "NombreCategoria",
        "Estado"]
    # Número de registros a mostrar por página en la lista del admin
    list_per_page = 10

# Organizamos los campos del formulario en secciones lógicas (informacion basica/informacion secundaria))
    fieldsets = (
        ('Datos importantes', {
            'fields': ('NombreCategoria','Estado')
        }),
        ('A detalle', {
            'fields': ('Descripcion', 'Observaciones')
        })
    )

    # Definimos los campos que serán solo lectura en el admin y qu eno se pueden editar
    readonly_fields = ['IdCategoriaProducto']
    
    #Llama al archivo js para la personalizacion de mensajes de guardado segun django admin
    class Media:
        js = ('js/confirmarGuardados.js',)


    # -------------------------------------------------------------
    # Se asigna el formulario específico del modelo para validar y 
    # manejar la creación/edición de registros de bodegas en el 
    # panel de admin.
    # -------------------------------------------------------------
    form = CategoriaProductoRegistracionForm

    # -------------------------------------------------------------
    # Método: save_model
    # Se ejecuta automáticamente al guardar un registro.
    # Permite detectar si se trata de una creación o una actualización
    # y mostrar mensajes personalizados al usuario.
    #
    # Parámetros:
    #   request -> objeto HTTP con la información del usuario actual.
    #   obj -> instancia del modelo que se está guardando.
    #   form -> formulario con los datos validados.
    #   change -> booleano que indica si el registro es nuevo (False)
    #             o está siendo editado (True).
    # -------------------------------------------------------------
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            # Si el registro es nuevo, muestra mensaje de creación
            self.message_user(request, f"La Categoria de Producto '{obj.NombreCategoria}' se ha creado.")
        if change:
            # Si el registro ya existía, muestra mensaje de actualización
            self.message_user(request, f"La Categoria de Producto '{obj.NombreCategoria}' se ha actualizado.")

    # -------------------------------------------------------------
    # Método: delete_model
    # Se ejecuta cuando se elimina un único registro desde la vista
    # de detalle del modelo en el administrador.
    #
    # Parámetros:
    #   request -> objeto HTTP actual.
    #   obj -> instancia del modelo que se está eliminando.
    #
    # Flujo:
    #   1. Obtiene el nombre (si existe).
    #   2. Llama al método original de eliminación.
    #   3. Muestra un mensaje de confirmación.
    # -------------------------------------------------------------
    def delete_model(self, request, obj):
        NombreCategoria = getattr(obj, 'NombreCategoria', str(obj))  # usa nombre si existe, o el objeto
        super().delete_model(request, obj)
        self.message_user(request, f"La Categoria de Producto '{NombreCategoria}' se ha eliminado.")

    # -------------------------------------------------------------
    # Método: delete_queryset
    # Se ejecuta cuando el usuario elimina varios registros a la vez
    # desde la lista del panel de administración (“Eliminar seleccionados”).
    #
    # Parámetros:
    #   request -> solicitud actual.
    #   queryset -> conjunto de registros seleccionados.
    #
    # Flujo:
    #   1. Cuenta cuántos registros se eliminarán.
    #   2. Llama al método base para eliminarlos.
    #   3. Muestra un mensaje con la cantidad de eliminados.
    # -------------------------------------------------------------
    def delete_queryset(self, request, queryset):
        count = queryset.count()
        super().delete_queryset(request, queryset)
        self.message_user(request, f"Se han eliminado {count} Categorias de Productos correctamente.")

# ========================================================================
# Registro del modelo en el panel de administración
# ========================================================================
# Esto permite que podamos gestionar los registros directamente
# desde el panel de administración de Django (crear, leer, actualizar y eliminar)
admin.site.register(CategoriaProducto, CategoriaProductoAdmin)