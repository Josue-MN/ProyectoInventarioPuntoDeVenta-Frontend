# ------------------------------------------------------------------------
# Importación de módulos y clases necesarias para el modelo
# ------------------------------------------------------------------------
# models: Permite definir clases que representan tablas de la base de datos.
# UniqueConstraint: Se utiliza para definir restricciones de unicidad a nivel de tabla.
# MinLengthValidator: Valida que el texto tenga una longitud mínima.
# ValidationError: Se usa para lanzar errores personalizados en las validaciones.
# re: Módulo de expresiones regulares, empleado para verificar formato de texto.
# ------------------------------------------------------------------------
from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
import re


# ========================================================================
# Modelo: CategoriaProducto
# ========================================================================
# Este modelo representa la tabla 'CategoriaProducto' en la base de datos.
# Cada campo del modelo se mapea directamente a una columna de dicha tabla.
# El parámetro db_column asegura que Django utilice los nombres exactos
# de las columnas existentes, evitando la creación de nuevas columnas por defecto.
# ========================================================================
class CategoriaProducto(models.Model):

    # --------------------------------------------------------------------
    # ID de la categoría de producto
    # --------------------------------------------------------------------
    # AutoField: genera automáticamente un valor incremental por cada registro.
    # primary_key=True: define este campo como la clave primaria.
    # db_column: asigna el nombre exacto de la columna en la base de datos.
    # verbose_name: define el nombre descriptivo que se mostrará en el panel admin.
    # --------------------------------------------------------------------
    IdCategoriaProducto = models.AutoField(
        primary_key=True,
        db_column='IdCategoriaProducto',
        verbose_name='Id Categoria Producto'
    )
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # FUNCIÓN: validacion_no_caracteres_especiales
    # --------------------------------------------------------------------
    # Esta función valida que el texto ingresado no contenga caracteres especiales.
    # Permite únicamente:
    #   - Letras (mayúsculas y minúsculas, incluyendo acentos y Ñ)
    #   - Números
    #   - Espacios
    # Si se ingresan caracteres no permitidos, lanza un ValidationError.
    # --------------------------------------------------------------------
    def validacion_no_caracteres_especiales(value):
        expresion = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$'
        if re.match(expresion, value):
            return value
        else:
            raise ValidationError('No se permiten caracteres especiales')
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # Nombre de la categoría
    # --------------------------------------------------------------------
    # CharField: campo de texto corto que almacena el nombre de la categoría.
    # max_length: longitud máxima de 20 caracteres.
    # db_column: nombre real de la columna en la base de datos.
    # verbose_name: etiqueta visible en formularios y panel administrativo.
    # validators:
    #   - validacion_no_caracteres_especiales: prohíbe símbolos o caracteres no válidos.
    #   - MinLengthValidator: obliga a ingresar al menos 5 caracteres.
    # --------------------------------------------------------------------
    NombreCategoria = models.CharField(
        max_length=20,
        db_column='NombreCategoria',
        verbose_name='Nombre de la categoria',
        validators=[
            validacion_no_caracteres_especiales,
            MinLengthValidator(3, message="Debes ingresar minimo 3 caracteres")
        ]
    )
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # Descripción de la categoría
    # --------------------------------------------------------------------
    # TextField: campo de texto largo, ideal para descripciones detalladas.
    # max_length: establece un límite máximo de 500 caracteres.
    # db_column: indica el nombre exacto de la columna en la base de datos.
    # verbose_name: nombre descriptivo mostrado en formularios.
    # validators:
    #   - validacion_no_caracteres_especiales: prohíbe símbolos o caracteres no válidos.
    #   - MinLengthValidator: obliga a ingresar al menos 10 caracteres.
    # --------------------------------------------------------------------
    Descripcion = models.TextField(
        max_length=500,
        db_column='Descripcion',
        verbose_name='Descripcion',
        validators=[
            validacion_no_caracteres_especiales,
            MinLengthValidator(10, message="Debes ingresar minimo 10 caracteres")
        ]
    )
    # --------------------------------------------------------------------
    # Lista de opciones posibles para el estado de la categoría
    ESTADO = [
        ('Activo', 'Activo'),      # La categoría está activa
        ('Pausado', 'Pausado'),    # La categoría está pausada
    ]

    # --------------------------------------------------------------------
    # Campo Estado del modelo
    Estado = models.CharField(
        max_length=10,    # Máxima longitud de 10 caracteres
        choices=ESTADO,   # Se limita a las opciones definidas en ESTADO
        db_column='Estado',  # Nombre de la columna en la base de datos
    )
    # --------------------------------------------------------------------

    # Campo Observaciones del modelo
    Observaciones = models.TextField(
        max_length=500,          # Máxima longitud de 500 caracteres
        db_column='Observaciones',  # Nombre de la columna en la base de datos
        verbose_name='Observaciones',  # Etiqueta legible para formularios y admin
        validators=[             # Validadores personalizados
            validacion_no_caracteres_especiales,  # No permite caracteres especiales
            MinLengthValidator(10, message="Debes ingresar minimo 10 caracteres")  # Requiere al menos 10 caracteres
        ]
    )

    # --------------------------------------------------------------------
    # Meta información del modelo
    # --------------------------------------------------------------------
    # Define configuraciones adicionales del modelo:
    #   - db_table: nombre exacto de la tabla en la base de datos.
    #   - constraints: restricciones de unicidad para evitar duplicados.
    # En este caso, garantiza que no existan dos categorías con el mismo ID.
    # --------------------------------------------------------------------
    class Meta:
        db_table = 'CategoriaProducto'
        constraints = [
            UniqueConstraint(fields=['IdCategoriaProducto'], name='unique_id_categoria_producto'),
        ]
        
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # MÉTODO __STR__ IMPLEMENTADO
    # --------------------------------------------------------------------
    # Devuelve una representación legible del objeto.
    # Es útil para mostrar registros de forma clara en el panel de administración
    # o en la shell de Django. Muestra los campos principales de la categoría.
    # --------------------------------------------------------------------
    def __str__(self):
        return f"NOMBRE: {self.NombreCategoria}, DESCRIPCION: {self.Descripcion}"
