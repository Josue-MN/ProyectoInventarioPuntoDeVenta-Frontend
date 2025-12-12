from django import forms
from CrudCargosApp.models import Cargos

# Definimos un formulario basado en el modelo 'Cargos'
class CargoRegistracionForm(forms.ModelForm):

    # Configuramos los metadatos del formulario
    class Meta:
        model = Cargos  # Indicamos que este formulario usa el modelo Cargos
        fields = '__all__'  # Incluye todos los campos del modelo en el formulario

        # Etiquetas personalizadas para mostrar nombres más claros en el formulario
        labels = {
            'TipoDeCargo': 'Tipo de cargo',
            'EstadoDelCargo': 'Estado del cargo',
            'DescripcionDelCargo': 'Descripción del cargo',
            'SueldoBase': 'Sueldo base'
        }

        # Textos de ayuda que se muestran debajo de los campos
        help_texts = {
            'TipoDeCargo': 'Seleccione el tipo de cargo',
            'EstadoDelCargo': 'Ingrese el estado del cargo a registrar',
            'DescripcionDelCargo': 'Ingrese una breve descripción de las funciones y responsabilidades del cargo',
            'SueldoBase': 'Ingrese el sueldo base correspondiente al cargo. Mínimo permitido: $150.000'
        }

        # Mensajes de error personalizados para validaciones automáticas
        error_messages = {
            'TipoDeCargo': {
                'required': 'Por favor seleccione un tipo de cargo disponibles',
            },
            'EstadoDelCargo': {
                'required': 'Por favor ingrese un estado del cargo a registrar',
            },
            'DescripcionDelCargo': {
                'required': 'Por favor ingrese una descripción del cargo.',
                'min_length': 'La descripción debe tener al menos 10 caracteres.'
            },
            'SueldoBase': {
                'required': 'Debe ingresar el sueldo base correspondiente.',
                'min_value': 'El sueldo base no puede ser menor a $150.000.'
            }
        }

        # Configuración de los widgets: definen cómo se muestran los campos en el HTML
        widgets = {
            'TipoDeCargo': forms.Select(attrs={
                'placeholder': 'Ej: Bodeguero'
            }),
            'EstadoDelCargo': forms.Select(attrs={
                'placeholder': 'Ej: Activo o Inactivo'
            }),
            'DescripcionDelCargo': forms.Textarea(attrs={
                'placeholder': 'Ej: Responsable de supervisar el orden, registro y entrega de productos dentro de la bodega.'
            }),
            'SueldoBase': forms.NumberInput(attrs={
                'placeholder': 'Ej: 450000'
            })
        }

    # --- VALIDACIONES PERSONALIZADAS ---

    # Esta función no aplica al modelo actual (NombreEmpleado no existe en Cargos)
    # Deberías eliminarla o cambiarla si no se usa.
    def clean_NombreEmpleado(self):
        inputNombre = self.cleaned_data['TipoDeCargo']
        if len(inputNombre) > 5:
            raise forms.ValidationError("El largo del nombre debe ser más de 5 caracteres")
        return inputNombre
    

    # Valida que la descripción tenga al menos 10 caracteres
    def clean_DescripcionDelCargo(self):
        inputDescripcionDelCargo = self.cleaned_data['DescripcionDelCargo'].strip()
        if len(inputDescripcionDelCargo) < 10:
            raise forms.ValidationError("La descripción del cargo debe tener al menos 10 caracteres")
        return inputDescripcionDelCargo
    

    # Lo ideal sería unir ambas condiciones en una sola función.
    def clean_DescripcionDelCargo(self):
        inputDescripcionDelCargo = self.cleaned_data['DescripcionDelCargo'].strip()
        if inputDescripcionDelCargo.isdigit():
            raise forms.ValidationError("La descripción no puede contener solo números")
        return inputDescripcionDelCargo


    # Valida que el sueldo base sea positivo
    def clean_SueldoBase(self):
        inputSueldoBase = self.cleaned_data['SueldoBase']
        if inputSueldoBase <= 0:
            raise forms.ValidationError("El sueldo base debe ser mayor a 0")
        return inputSueldoBase
