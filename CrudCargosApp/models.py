# ------------------------------------------------------------------------
# Importación de módulos y clases necesarias para el modelo
# ------------------------------------------------------------------------
# models: Permite definir clases que representan tablas en la base de datos.
# UniqueConstraint: Se utiliza para establecer restricciones de unicidad a nivel de tabla.
# MinLengthValidator: Valida que el texto cumpla una longitud mínima.
# ------------------------------------------------------------------------
from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MinLengthValidator, MinValueValidator


# ========================================================================
# Modelo: Cargos
# ========================================================================
# Este modelo representa la tabla 'Cargos' en la base de datos.
# Cada atributo de la clase se mapea directamente a una columna de dicha tabla.
# El uso de db_column asegura que los nombres de las columnas coincidan exactamente
# con los de la base de datos, evitando que Django cree nombres por defecto.
# ========================================================================
class Cargos(models.Model):

    
    # --------------------------------------------------------------------
    # ID del cargo
    # --------------------------------------------------------------------
    # AutoField: crea un campo autoincremental único por cada registro.
    # primary_key=True: lo define como la clave primaria de la tabla.
    # db_column: indica el nombre exacto del campo en la base de datos.
    # verbose_name: etiqueta legible que se muestra en el panel de administración.
    # --------------------------------------------------------------------
    IdCargos = models.AutoField(
        primary_key=True,
        db_column='IdCargos',
        verbose_name='Id Cargo'
    )
    # --------------------------------------------------------------------

    # --------------------------------------------------------------------
    # OPCIONES DISPONIBLES: Tipo de Cargo
    # --------------------------------------------------------------------
    # Se define una lista de tuplas con las opciones posibles para el campo TipoDeCargo.
    # Este patrón se usa con el parámetro 'choices' para restringir los valores válidos.
    # Ejemplo:
    #   - 'Gerente'
    #   - 'Bodeguero'
    # --------------------------------------------------------------------
    TIPO_DE_CARGO = [
        ('Etiquetador', 'Etiquetador'),
        ('Bodeguero', 'Bodeguero'),
        ('Ayudante', 'Ayudante'),
        ('Despachador', 'Despachador'),
    ]
    # --------------------------------------------------------------------

    # --------------------------------------------------------------------
    # Tipo de cargo
    # --------------------------------------------------------------------
    # CharField: almacena el tipo de cargo en formato de texto.
    # max_length: limita el número máximo de caracteres (10).
    # choices: define un conjunto cerrado de valores válidos (TIPO_DE_CARGO).
    # db_column: nombre de la columna en la base de datos.
    # verbose_name: nombre descriptivo mostrado en la interfaz del admin.
    # --------------------------------------------------------------------
    TipoDeCargo = models.CharField(
        max_length=20,
        choices=TIPO_DE_CARGO,
        db_column='TipoDeCargo',
        verbose_name='Tipo de cargo'
    )
    # --------------------------------------------------------------------

    ESTADOS = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    # --------------------------------------------------------------------
    # Estado del cargo
    # --------------------------------------------------------------------
    # CharField: almacena el estado actual del cargo (por ejemplo: "Activo", "Inactivo").
    # max_length: longitud máxima de 20 caracteres.
    # db_column: nombre real de la columna en la base de datos.
    # verbose_name: etiqueta visible en formularios y el panel administrativo.
    # validators:
    #   - MinLengthValidator: asegura que el texto tenga al menos 4 caracteres.
    # --------------------------------------------------------------------
    EstadoDelCargo = models.CharField(
        max_length=10,
        choices=ESTADOS,
        db_column='EstadoDelCargo',
        verbose_name='Estado del cargo'
    )
    # --------------------------------------------------------------------


    # Campo para almacenar la descripción del cargo
    DescripcionDelCargo = models.TextField(
        max_length=500,  # Máximo de 500 caracteres
        db_column='DescripcionDelCargo',  # Nombre de la columna en la base de datos
        verbose_name='Descripcion del cargo',  # Nombre legible en el admin
        validators=[MinLengthValidator(10, message='Debe ingresar al menos 10 caracteres')]  # Valida que tenga al menos 10 caracteres
    )

    # Campo para almacenar el sueldo base del cargo
    SueldoBase = models.IntegerField(
        db_column='SueldoBase',  # Nombre de la columna en la base de datos
        verbose_name='Sueldo base',  # Nombre legible en el admin
        validators=[MinValueValidator(150000, message='Sueldo base minimo es de $150.000')]  # Valida que sea mínimo $150.000
    )

    # --------------------------------------------------------------------
    # Meta información del modelo
    # --------------------------------------------------------------------
    # Define configuraciones adicionales de la clase:
    #   - db_table: nombre exacto de la tabla que Django debe usar.
    #   - constraints: define restricciones de unicidad a nivel de tabla.
    # En este caso, asegura que el IdCargos no se repita en la tabla.
    # --------------------------------------------------------------------
    class Meta:
        db_table = 'Cargos'
        constraints = [
            UniqueConstraint(fields=['IdCargos'], name='unique_id_cargos'),
        ]
    # --------------------------------------------------------------------


    # --------------------------------------------------------------------
    # MÉTODO __STR__ IMPLEMENTADO
    # --------------------------------------------------------------------
    # Este método devuelve una representación legible del objeto.
    # Es útil para mostrar la información en el panel de administración
    # y para depuración, mostrando los datos principales del cargo.
    # --------------------------------------------------------------------
    def __str__(self):
        return f"Tipo de Cargo: {self.TipoDeCargo}, Descripcion del cargo: {self.DescripcionDelCargo}, Sueldo base: {self.SueldoBase}"
