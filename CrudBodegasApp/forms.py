from django import forms
from CrudBodegasApp.models import Bodegas
import re

# Importa las herramientas necesarias de Django para crear formularios basados en modelos
class BodegaRegistracionForm(forms.ModelForm):
    """
    Formulario para registrar y validar los datos del modelo 'Bodegas'.
    Se encarga de mostrar etiquetas personalizadas, mensajes de error,
    y validaciones específicas para ciertos campos.
    """

    class Meta:
        # Indica que este formulario está basado en el modelo 'Bodegas'
        model = Bodegas

        # Incluye todos los campos del modelo
        fields = '__all__'

        # Etiquetas personalizadas que se mostrarán en el formulario
        labels = {
            'NombreBodega': 'Nombre de la bodega',
            'UbicacionBodega': 'Ubicación de la bodega',
            'EstadoBodega': 'Estado de la bodega',
            'ObservacionesBodega': 'Observaciones sobre la bodega',
        }

        # Mensajes de ayuda que aparecerán como texto explicativo en el formulario
        help_texts = {
            'NombreBodega': 'Ingrese el nombre de la bodega',
            'UbicacionBodega': 'Indique la ubicación de la bodega',
            'EstadoBodega': 'Seleccione el estado actual de la bodega (Activa, Inactiva o En Mantenimiento)',
            'ObservacionesBodega': 'Ingrese detalles adicionales o notas relevantes sobre la bodega',
        }

        # Mensajes de error personalizados que se mostrarán si ocurre una validación fallida
        error_messages = {
            'NombreBodega': {
                'required': 'Por favor ingrese un nombre a la bodega',
            },
            'UbicacionBodega': {
                'required': 'Por favor ingrese la ubicación de la bodega',
            },
            'EstadoBodega': {
                'required': 'Debe seleccionar un estado para la bodega.',
            },
            'ObservacionesBodega': {
                'required': 'Por favor ingrese una observación o nota descriptiva.',
                'min_length': 'Las observaciones deben tener al menos 10 caracteres.',
            },
        }

        # Personalización de los widgets (apariencia y comportamiento de los campos en el formulario)
        widgets = {
            'NombreBodega': forms.TextInput(attrs={
                'placeholder': 'Ej: Bodega norte'
            }),
            'UbicacionBodega': forms.TextInput(attrs={
                'placeholder': 'Ej: Primer piso'
            }),
            'EstadoBodega': forms.Select(attrs={
                'placeholder': 'Ej: Inactivo'
            }),
            'ObservacionesBodega': forms.Textarea(attrs={
                'placeholder': 'Ej: Se utiliza para productos perecibles o de rotación rápida.'
            }),
        }

    # ---------------------------
    # VALIDACIONES PERSONALIZADAS
    # ---------------------------

    def clean_NombreBodega(self):
        """
        Limpia y valida el campo 'NombreBodega'.
        - Elimina espacios innecesarios.
        - Convierte el texto a formato Título (primera letra mayúscula).
        - Verifica que solo contenga letras, números o espacios válidos.
        """
        inputNombreBodega = self.cleaned_data['NombreBodega'].strip().upper().title()

        # Expresión regular: permite letras y números, pero no mezcla de ambos sin espacio
        caracteres = r"^(?:\d+|[A-ZÁÉÍÓÚÑa-záéíóúñ]{2,})(?: (?:\d+|[A-ZÁÉÍÓÚÑa-záéíóúñ]{2,}))*$"

        # Si el texto no cumple con el patrón, muestra error
        if not re.match(caracteres, inputNombreBodega):
            raise forms.ValidationError(
                "Ingrese un nombre de bodega sin caracteres especiales, "
                "con más de 5 letras, sin juntar números ni letras y sin más de un espacio entre palabras."
            )
        return inputNombreBodega  # Devuelve el valor limpio si es válido

    def clean_UbicacionBodega(self):
        """
        Limpia y valida el campo 'UbicacionBodega'.
        - Elimina espacios.
        - Convierte a formato Título.
        - Valida caracteres permitidos.
        """
        inputUbicacionBodega = self.cleaned_data['UbicacionBodega'].strip().upper().title()
        caracteres = r"^(?:\d+|[A-ZÁÉÍÓÚÑa-záéíóúñ]{2,})(?: (?:\d+|[A-ZÁÉÍÓÚÑa-záéíóúñ]{2,}))*$"

        if not re.match(caracteres, inputUbicacionBodega):
            raise forms.ValidationError(
                "Ingrese la ubicación de la bodega sin caracteres especiales, "
                "con más de 5 letras, sin juntar números ni letras y sin más de un espacio entre palabras."
            )
        return inputUbicacionBodega

    def clean_ObservacionesBodega(self):
        """
        Valida el campo 'ObservacionesBodega'.
        - Debe tener al menos 10 caracteres.
        - No puede contener solo números.
        """
        inputObservacionesBodega = self.cleaned_data['ObservacionesBodega']

        # Longitud mínima
        if len(inputObservacionesBodega) < 10:
            raise forms.ValidationError("La observación debe tener al menos 10 caracteres.")
        
        # No permitir solo números
        if inputObservacionesBodega.isdigit():
            raise forms.ValidationError("La observación no puede contener solo números.")
        
        return inputObservacionesBodega
