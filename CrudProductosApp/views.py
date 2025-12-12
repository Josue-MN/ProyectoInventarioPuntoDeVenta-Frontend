# Importaciones necesarias
from django.shortcuts import render, redirect  # 'render' para mostrar templates y 'redirect' para redirigir
from django.contrib import messages
from AuditoriaApp.views import RegistrarAuditoriaProducto
from LoginApp.decorators import login_requerido

# ========================================================================
# VISTA: Mostrar todos los productos
# ========================================================================
@login_requerido
def productosData(request):
    """
    Obtiene todos los registros de productos de la base de datos
    y los envía al template 'producto-models.html' para mostrarlos.

    Parámetros:
    - request: Objeto HttpRequest que contiene información sobre la solicitud HTTP.

    Retorna:
    - render: Renderiza el template con los datos de los productos.
    """
    productos = Productos.objects.all()  # Consulta todos los productos
    data = {'Productos': productos}  # Diccionario con los datos para el template
    return render(request, 'templateCrudProducto/productos-models.html', data)


# ========================================================================
# VISTA: Registro de un nuevo producto
# ========================================================================
@login_requerido
def productosRegistrationView(request):
    """
    Permite registrar un nuevo producto mediante un formulario.
    Si la solicitud es POST y el formulario es válido, guarda los datos
    y redirige a la página de listado de productos.

    Parámetros:
    - request: Objeto HttpRequest que contiene información sobre la solicitud HTTP.

    Retorna:
    - render: Renderiza el template 'registro-producto.html' con el formulario.
    """
    form = forms.ProductoRegistrationForm()  # Inicializa un formulario vacío

    if request.method == 'POST':  # Verifica si se envió el formulario
        form = forms.ProductoRegistrationForm(request.POST)  # Crea un formulario con los datos enviados
        if form.is_valid():  # Valida los datos del formulario
            # Imprime en consola los datos validados para depuración
            print("FORM ES VALIDO")
            print("CODIGO DE BARRAS: ", form.cleaned_data['CodigoDeBarras'])
            print("VALOR: ", form.cleaned_data['ValorProducto'])
            print("STOCK: ", form.cleaned_data['StockProducto'])
            print("NOMBRE DEL PRODUCTO: ", form.cleaned_data['NombreProducto'])
            print("MARCA: ", form.cleaned_data['MarcaProducto'])
            print("FECHA DE VENCIMIENTO: ", form.cleaned_data['FechaDeVencimiento'])
            print("CATEGORIA DEL PRODUCTO: ", form.cleaned_data['CategoriaProducto'])
            print("BODEGA ASOCIADA: ", form.cleaned_data['Bodegas'])

            producto_nuevo = form.save()  # Guarda el nuevo producto en la base de datos
            RegistrarAuditoriaProducto(request, producto_nuevo, "REGISTRAR")
            messages.success(request, "Producto registrado correctamente")
            
            # ========================================================================
            # METODO DE REDIRECCION MEDIANTE USUARIO LOGGEADO
            # ========================================================================
            UsuarioLogeado = request.session.get('Usuario_Username')
            if UsuarioLogeado == "Admin":
                #Accede a la ruta nombrada de urls_admin.py, nombrada como name='admin-crud-producto'
                return redirect('admin-crud-producto')
            else:
                return redirect('crud-producto')
            # ========================================================================
        else:
            messages.error(request, "Corrige los errores en el formulario antes de continuar")
    
    data = {'form': form,}  # Diccionario con el formulario
    return render(request, 'templateCrudProducto/registro-producto.html', data)


# ========================================================================
# VISTA: Actualizar un producto existente
# ========================================================================
@login_requerido
def actualizarProducto(request, IdProducto):
    """
    Permite actualizar los datos de un producto existente.

    Parámetros:
    - request: Objeto HttpRequest con información de la solicitud.
    - IdProducto: Identificador único del producto a actualizar.

    Retorna:
    - render: Renderiza el template 'registro-producto.html' con el formulario.
    """
    producto = Productos.objects.get(IdProducto=IdProducto)  # Obtiene el producto por su ID
    form = forms.ProductoRegistrationForm(instance=producto)  # Formulario precargado con datos del producto

    if request.method == 'POST':  # Si se envían datos para actualizar
        form = forms.ProductoRegistrationForm(request.POST, instance=producto)
        if form.is_valid():
            producto_actualizar = form.save()  # Guarda los cambios en la base de datos
            RegistrarAuditoriaProducto(request, producto_actualizar, "ACTUALIZAR")
            messages.success(request, "Producto Actualizado correctamente")

            # ========================================================================
            # METODO DE REDIRECCION MEDIANTE USUARIO LOGGEADO
            # ========================================================================
            UsuarioLogeado = request.session.get('Usuario_Username')
            if UsuarioLogeado == "Admin":
                #Accede a la ruta nombrada de urls_admin.py, nombrada como name='admin-crud-producto'
                return redirect('admin-crud-producto')
            else:
                return redirect('crud-producto')
            # ========================================================================
        else:
            messages.error(request, "Corrige los errores en el formulario antes de continuar")
            
    data = {'form': form,}  # Diccionario con el formulario
    return render(request, 'templateCrudProducto/registro-producto.html', data)


# ========================================================================
# VISTA: Eliminar un producto
# ========================================================================

@login_requerido
def confirmarEliminar(request, IdProducto):
    producto = Productos.objects.get(IdProducto=IdProducto)
    data = {'pro' : producto}
    return render(request, 'templateCrudProducto/confirmar-eliminar.html', data)

@login_requerido
def eliminarProducto(request, IdProducto):
    producto = Productos.objects.get(IdProducto=IdProducto)
    if request.method == 'POST':
        RegistrarAuditoriaProducto(request, producto, "ELIMINAR")
        producto.delete()
        messages.success(request, f"El producto '{producto.NombreProducto}' fue eliminado correctamente.")
        
        # ========================================================================
        # METODO DE REDIRECCION MEDIANTE USUARIO LOGGEADO
        # ========================================================================
        UsuarioLogeado = request.session.get('Usuario_Username')
        if UsuarioLogeado == "Admin":
            #Accede a la ruta nombrada de urls_admin.py, nombrada como name='admin-crud-producto'
            return redirect('admin-crud-producto')
        else:
            return redirect('crud-producto')
        # ========================================================================
    else:
        messages.error(request, "Método no permitido para eliminar usuarios.")

#Detalle
@login_requerido
def detalleProducto(request, IdProducto):
    producto = Productos.objects.get(IdProducto=IdProducto)
    data = {'pro' : producto}
    return render(request, 'templateCrudProducto/detalle-producto.html', data)