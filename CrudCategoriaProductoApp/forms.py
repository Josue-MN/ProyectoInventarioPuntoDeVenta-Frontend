from django import forms
from CrudCategoriaProductoApp.models import CategoriaProducto

# Formulario de registro para el modelo CategoriaProducto
class CategoriaProductoRegistracionForm(forms.ModelForm):

    class Meta:
        model = CategoriaProducto  # Modelo asociado al formulario
        fields = '__all__'  # Se incluyen todos los campos del modelo

        # Etiquetas personalizadas para los campos del formulario
        labels = {
            'NombreCategoria': 'Nombre de la categoria',
            'Descripcion': 'Descripcion',
            'Estado': 'Estado de la categoría',
            'Observaciones': 'Observaciones'
        }

        # Textos de ayuda que aparecerán en la interfaz del formulario
        help_texts = {
            'NombreCategoria': 'Indique el nombre de la categoria a registrar',
            'Descripcion': 'Ingrese la descripcion sobre la categoria a registrar',
            'Estado': 'Seleccione si la categoría está actualmente activa o pausada.',
            'Observaciones': 'Incluya cualquier detalle adicional o nota administrativa relevante.'
        }

        # Mensajes de error personalizados para cada campo
        error_messages = {
            'NombreCategoria': {
                'required': 'Por favor introduzca un nombre a la categoria',
            },
            'Descripcion': {
                'required': 'Por favor ingrese una descripcion a la categoria a registrar',
            },
            'Estado': {
                'required': 'Debe seleccionar un estado para la categoría.'
            },
            'Observaciones': {
                'required': 'Por favor ingrese una observación o comentario.',
                'min_length': 'Las observaciones deben tener al menos 10 caracteres.'
            }
        }

        # Widgets personalizados para los campos (placeholders, tipo de input, etc.)
        widgets = {
            'NombreCategoria': forms.TextInput(attrs={
                'placeholder': 'Ej: Snacks'
            }),
            'Descripcion': forms.Textarea(attrs={
                'placeholder': 'Ej: Categoría destinada a productos de consumo inmediato o ligero'
            }),
            'Estado': forms.Select(attrs={
                'placeholder': 'Ej: Inactivo'
            }),
            'Observaciones': forms.Textarea(attrs={
                'placeholder': 'Ej: Esta categoría se usa para productos exhibidos en mostrador.',
            })
        }
    
    # Validación personalizada para el campo NombreCategoria
    def clean_NombreCategoria(self):
        inputNombre = self.cleaned_data['NombreCategoria']  # Obtiene el valor del campo
        if len(inputNombre) < 3:  # Valida que tenga al menos 3 caracteres
            raise forms.ValidationError("El largo del nombre de la categoria debe ser mas de 3 caracteres")
        return inputNombre  # Retorna el valor limpio si es válido
    
    # Validación personalizada para el campo Descripcion
    def clean_Descripcion(self):
        inputDescripcion = self.cleaned_data['Descripcion'].strip()  # Elimina espacios al inicio y fin
        if len(inputDescripcion) < 10:  # Valida longitud mínima
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return inputDescripcion  # Retorna el valor limpio si es válido

    # Validación personalizada para el campo Observaciones
    def clean_Observaciones(self):
        inputObservaciones = self.cleaned_data['Observaciones'].strip()  # Elimina espacios al inicio y fin
        if len(inputObservaciones) < 10:  # Valida longitud mínima
            raise forms.ValidationError("Las observaciones deben tener al menos 10 caracteres.")
        return inputObservaciones  # Retorna el valor limpio si es válido
