# ------------------------------------------------------------------------
# Importación de módulos y clases necesarias para el modelo
# ------------------------------------------------------------------------
# models: Permite definir clases que representan tablas en la base de datos.
# UniqueConstraint: Permite definir restricciones de unicidad entre campos.
# Validadores: Se utilizan para imponer límites mínimos de valor o longitud.
# timezone: Permite manejar fechas y horas con conocimiento del huso horario.
# ValidationError: Se usa para lanzar errores personalizados durante la validación.
# ------------------------------------------------------------------------
from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MinLengthValidator, MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from CrudCategoriaProductoApp.models import CategoriaProducto #Se importa el models para hacer uso de la llave foranea

# ========================================================================
# Modelo: Productos
# ========================================================================
# Representa la tabla 'Productos' en la base de datos.
# Cada atributo de la clase corresponde a una columna de la tabla.
# Se usa db_column para mapear cada campo a una columna específica
# existente en la base de datos, evitando que Django genere nombres automáticos.
# ========================================================================
class Productos(models.Model):

    # --------------------------------------------------------------------
    # ID del producto
    # --------------------------------------------------------------------
    # AutoField: campo autoincremental que genera automáticamente un valor único.
    # primary_key=True: define el campo como clave primaria de la tabla.
    # db_column: nombre exacto de la columna en la base de datos.
    # --------------------------------------------------------------------
    IdProducto = models.AutoField(
        primary_key=True,
        db_column='IdProducto'
    )
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # Código de barras del producto
    # --------------------------------------------------------------------
    # CharField: campo de texto de longitud variable.
    # max_length: define el número máximo de caracteres permitidos (100).
    # db_column: nombre de la columna en la base de datos.
    # verbose_name: texto descriptivo mostrado en formularios o panel de admin.
    # error_messages: mensaje personalizado en caso de violar una restricción.
    # --------------------------------------------------------------------
    CodigoDeBarras = models.CharField(
        max_length=100,
        db_column='CodigoDeBarras',
        verbose_name="Código de Barras",
        error_messages={'unique': 'El código de barras ingresado ya se encuentra registrado. Por favor, verifique.'}
    )
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # Valor del producto
    # --------------------------------------------------------------------
    # IntegerField: campo numérico entero que almacena el valor monetario.
    # validators: asegura que el valor mínimo permitido sea $1000.
    # verbose_name: texto legible que se muestra en el panel de administración.
    # --------------------------------------------------------------------
    ValorProducto = models.IntegerField(
        db_column='ValorProducto',
        verbose_name="Valor",
        validators=[MinValueValidator(1000, message="El valor minimo de un producto es de $1000")]
    )
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # Stock del producto
    # --------------------------------------------------------------------
    # IntegerField: campo numérico entero que almacena la cantidad disponible.
    # validators: establece que debe haber al menos 1 unidad en stock.
    # verbose_name: nombre descriptivo mostrado en la interfaz administrativa.
    # --------------------------------------------------------------------
    StockProducto = models.IntegerField(
        db_column='StockProducto',
        verbose_name="Stock",
        validators=[MinValueValidator(1, message="El Stock minimo es de 1 unidad ")]
    )
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # Nombre del producto
    # --------------------------------------------------------------------
    # CharField: campo de texto para el nombre.
    # max_length: establece un máximo de 60 caracteres.
    # validators: obliga a que el nombre tenga al menos 5 caracteres.
    # --------------------------------------------------------------------
    NombreProducto = models.CharField(
        max_length=60,
        db_column='NombreProducto',
        verbose_name="Nombre del producto",
        validators=[MinLengthValidator(5, message="El nombre del producto debe tener al menos 5 caracteres.")]
    )
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # Fecha de registro del producto
    # --------------------------------------------------------------------
    # DateTimeField: almacena fecha y hora.
    # auto_now_add=True: Django asigna automáticamente la fecha y hora actuales
    # cuando el producto se crea por primera vez.
    # db_column: nombre de la columna en la base de datos.
    # --------------------------------------------------------------------
    FechaDeRegistroProducto = models.DateTimeField(
        auto_now_add=True,
        db_column='FechaDeRegistroProducto'
    )
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # Marca del producto
    # --------------------------------------------------------------------
    # CharField: texto para la marca del producto.
    # max_length: hasta 55 caracteres.
    # validators: obliga a que la marca tenga al menos 4 letras.
    # verbose_name: etiqueta visible en formularios.
    # --------------------------------------------------------------------
    MarcaProducto = models.CharField(
        max_length=55,
        db_column='MarcaProducto',
        verbose_name="Marca",
        validators=[MinLengthValidator(4, message="La marca del producto debe tener al menos 4 caracteres")]
    )
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # FUNCIÓN: validacion_fecha_de_vencimiento_futura
    # --------------------------------------------------------------------
    # Esta función asegura que la fecha de vencimiento ingresada sea posterior
    # a la fecha actual. Si la fecha es anterior o igual a hoy, se lanza un error.
    # Esto previene el registro de productos ya vencidos.
    # --------------------------------------------------------------------
    def validacion_fecha_de_vencimiento_futura(value):
        if value <= timezone.now().date():
            raise ValidationError('La fecha ingresada no es una fecha futura.')
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # Fecha de vencimiento del producto
    # --------------------------------------------------------------------
    # DateField: almacena solo la fecha (sin hora).
    # validators: aplica la función anterior para evitar fechas pasadas o iguales a hoy.
    # verbose_name: etiqueta amigable para formularios y panel de administración.
    # --------------------------------------------------------------------
    FechaDeVencimiento = models.DateField(
        db_column='FechaDeVencimiento',
        verbose_name="Fecha de vencimiento",
        validators=[validacion_fecha_de_vencimiento_futura]
    )
    # --------------------------------------------------------------------

    ###LLAVE FORANEA###
    CategoriaProducto = models.ForeignKey(
        CategoriaProducto, #Modelo Relacionado
        on_delete=models.SET_NULL,
        related_name="producto", #Para acceder a el desde categoria
        db_column="CategoriaProductoId", #Nombre que tendra en la base de datos
        null=True, #Si puede quedar nulo
        blank=True #Si puede quedar vacio
        #SI NULL Y BLANK QUEDAN EN FALSE LA VALIDACION PERSONALIZADA QUEDA INACTIVA
    )
    #models.CASCADE → borra también el relacionado.
    #models.PROTECT → impide borrarlo si está en uso.
    #models.SET_NULL → pone NULL en la FK.
    #models.SET_DEFAULT → asigna valor por defecto

    #default="Sin valor", #Lo que ocurrre segun la lista de abajo si se elimina

    Bodegas = models.ForeignKey(
        Bodegas,
        on_delete=models.SET_NULL,
        related_name="producto",
        db_column="BodegaId",
        null=True,
        blank=True
    )


    # --------------------------------------------------------------------
    # Meta información del modelo
    # --------------------------------------------------------------------
    # La clase Meta se usa para definir configuraciones adicionales del modelo:
    #   - db_table: nombre exacto de la tabla en la base de datos.
    #   - constraints: establece reglas de unicidad para evitar duplicados.
    #     En este caso, ningún IdProducto ni CodigoDeBarras puede repetirse.
    # --------------------------------------------------------------------
    class Meta:
        db_table = 'Productos'
        constraints = [
            UniqueConstraint(fields=['IdProducto'], name='unique_id_producto'),
            UniqueConstraint(fields=['CodigoDeBarras'], name='unique_codigo_de_barras'),
        ]
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # MÉTODO __STR__ IMPLEMENTADO
    # --------------------------------------------------------------------
    # Este método define cómo se mostrará un objeto Producto cuando se imprima.
    # Se utiliza principalmente en el panel de administración o en consola.
    # Devuelve una cadena legible con la información principal del producto.
    # --------------------------------------------------------------------
    def __str__(self):
        return f"ID: {self.IdProducto}, NOMBRE: {self.NombreProducto}, CODIGO DE BARRAS: {self.CodigoDeBarras}, VALOR: {self.ValorProducto}, STOCK: {self.StockProducto}, MARCA: {self.MarcaProducto}, FECHA DE REGISTRO: {self.FechaDeRegistroProducto}, FECHA DE VENCIMIENTO: {self.FechaDeVencimiento}, CATEGORIA PRODUCTO: {self.CategoriaProducto}, BODEGA ASOCIADA: {self.Bodegas}"
    
    