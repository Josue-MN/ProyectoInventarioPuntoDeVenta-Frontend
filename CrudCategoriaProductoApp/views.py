from django.shortcuts import render, redirect
from django.contrib import messages
from AuditoriaApp.views import RegistrarAuditoriaCategoria
from LoginApp.decorators import login_requerido


# Create your views here.

# --------------------------------------------------------------------
# Vista para mostrar todos los registros de CategoriaProducto
@login_requerido
def categoriaProductoData(request):
    # Obtiene todos los objetos de la tabla CategoriaProducto
    categoriaProducto = CategoriaProducto.objects.all()
    
    # Prepara los datos para enviarlos al template
    data = {'CategoriaProducto': categoriaProducto}
    
    # Renderiza la plantilla con los datos
    return render(request, 'templateCrudCategoriaProducto/categoriaProducto-models.html', data)

# --------------------------------------------------------------------
# Vista para registrar una nueva categoría de producto
@login_requerido
def categoriaProductoRegistracionView(request):
    # Inicializa el formulario vacío
    form = forms.CategoriaProductoRegistracionForm()

    # Verifica si se envió un POST (cuando se envía el formulario)
    if request.method == 'POST':
        form = forms.CategoriaProductoRegistracionForm(request.POST)
        if form.is_valid():  # Si el formulario es válido
            # Imprime los datos en consola (para depuración)
            print("FORM VALIDO")
            print("NOMBRE: ", form.cleaned_data['NombreCategoria'])
            print("DESCRIPCION: ", form.cleaned_data['Descripcion'])
            print("ESTADO: ", form.cleaned_data['Estado'])
            print("OBSERVACIONES: ", form.cleaned_data['Observaciones'])

            # Guarda el nuevo registro en la base de datos
            categoria_nueva = form.save()
            RegistrarAuditoriaCategoria(request, categoria_nueva, "REGISTRAR")
            # Muestra mensaje de éxito en la interfaz
            messages.success(request, "Categoria registrada correctamente")

            # ========================================================================
            # METODO DE REDIRECCION MEDIANTE USUARIO LOGGEADO
            # ========================================================================
            UsuarioLogeado = request.session.get('Usuario_Username')
            if UsuarioLogeado == "Admin":
                #Accede a la ruta nombrada de urls_admin.py, nombrada como name='admin-crud-producto'
                return redirect('admin-crud-categoria')
            else:
                return redirect('crud-categoria')
            # ========================================================================
        else:
            # Muestra mensaje de error si el formulario no es válido
            messages.error(request, "Corrige los errores en el formulario antes de continuar")
    
    # Datos a enviar al template
    data = {'form': form}
    return render(request, 'templateCrudCategoriaProducto/registro-categoriaProducto.html', data)

# --------------------------------------------------------------------
# Vista para actualizar una categoría de producto existente
@login_requerido
def actualizarCategoriaProducto(request, IdCategoriaProducto):
    # Obtiene el registro específico según su ID
    categoriaProducto = CategoriaProducto.objects.get(IdCategoriaProducto=IdCategoriaProducto)
    # Inicializa el formulario con los datos existentes
    form = forms.CategoriaProductoRegistracionForm(instance=categoriaProducto)

    if request.method == 'POST':
        # Vuelve a inicializar el formulario con los datos enviados
        form = forms.CategoriaProductoRegistracionForm(request.POST, instance=categoriaProducto)
        if form.is_valid():  # Si los datos son válidos
            categoria_actualizar = form.save()  # Guarda los cambios
            RegistrarAuditoriaCategoria(request, categoria_actualizar, "ACTUALIZAR")
            messages.success(request, "Categoria actualizada correctamente")

            # ========================================================================
            # METODO DE REDIRECCION MEDIANTE USUARIO LOGGEADO
            # ========================================================================
            UsuarioLogeado = request.session.get('Usuario_Username')
            if UsuarioLogeado == "Admin":
                #Accede a la ruta nombrada de urls_admin.py, nombrada como name='admin-crud-producto'
                return redirect('admin-crud-categoria')
            else:
                return redirect('crud-categoria')
            # ========================================================================
        else:
            messages.error(request, "Corrige los errores en el formulario antes de continuar")
    
    # Datos a enviar al template
    data = {'form': form}
    return render(request, 'templateCrudCategoriaProducto/registro-categoriaProducto.html', data)

# --------------------------------------------------------------------
# Vista para mostrar la confirmación antes de eliminar
@login_requerido
def confirmarEliminar(request, IdCategoriaProducto):
    # Obtiene la categoría a eliminar según su ID
    categoriaProducto = CategoriaProducto.objects.get(IdCategoriaProducto=IdCategoriaProducto)
    
    # Envía el objeto al template de confirmación
    data = {'bod' : categoriaProducto}
    return render(request, 'templateCrudCategoriaProducto/confirmar-eliminar.html', data)

# --------------------------------------------------------------------
# Vista para eliminar la categoría de producto
@login_requerido
def eliminarCategoriaProducto(request, IdCategoriaProducto):
    # Obtiene la categoría a eliminar
    categoriaProducto = CategoriaProducto.objects.get(IdCategoriaProducto=IdCategoriaProducto)
    
    if request.method == 'POST':  # Solo permite eliminación vía POST
        RegistrarAuditoriaCategoria(request, categoriaProducto, "ELIMINAR")
        categoriaProducto.delete()  # Elimina el registro
        messages.success(request, f"La categoria '{categoriaProducto.NombreCategoria}' fue eliminado correctamente.")
        
        # ========================================================================
        # METODO DE REDIRECCION MEDIANTE USUARIO LOGGEADO
        # ========================================================================
        UsuarioLogeado = request.session.get('Usuario_Username')
        if UsuarioLogeado == "Admin":
            #Accede a la ruta nombrada de urls_admin.py, nombrada como name='admin-crud-producto'
            return redirect('admin-crud-categoria')
        else:
            return redirect('crud-categoria')
        # ========================================================================
    else:
        # Si no es método POST, muestra mensaje de error
        messages.error(request, "Método no permitido para eliminar usuarios.")

# --------------------------------------------------------------------
# Vista para mostrar el detalle de una categoría de producto
@login_requerido
def detalleCategoriaProducto(request, IdCategoriaProducto):
    # Obtiene la categoría específica
    categoriaProducto = CategoriaProducto.objects.get(IdCategoriaProducto=IdCategoriaProducto)
    
    # Envía el objeto al template de detalle
    data = {'bod' : categoriaProducto}
    return render(request, 'templateCrudCategoriaProducto/detalle-categoriaProducto.html', data)
