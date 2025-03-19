from django import forms
from .models import Transaccion, Categoria, Subcategoria

class TransaccionForm(forms.ModelForm):
    # Campo para la escala del monto
    MULTIPLICADOR_CHOICES = [
        ('1', 'Unidades'),
        ('1000', 'Miles'),
        ('1000000', 'Millones'),
    ]
    multiplicador = forms.ChoiceField(choices=MULTIPLICADOR_CHOICES, initial='1', label='Escala del Monto')

    # Campos de ayuda para filtrar
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]
    MODALIDAD_CHOICES = [
        ('fijo', 'Fijo'),
        ('variable', 'Variable'),
    ]
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, label='Tipo')
    modalidad = forms.ChoiceField(choices=MODALIDAD_CHOICES, label='Modalidad')

    class Meta:
        model = Transaccion
        fields = ['monto', 'multiplicador', 'tipo', 'modalidad', 'categoria', 'subcategoria', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si hay datos (POST), actualizamos los querysets según los valores enviados
        if self.data.get('tipo') and self.data.get('modalidad'):
            tipo_val = self.data.get('tipo')
            modalidad_val = self.data.get('modalidad')
            self.fields['categoria'].queryset = Categoria.objects.filter(
                tipo=tipo_val,
                subcategorias__modalidad=modalidad_val
            ).distinct()
        else:
            self.fields['categoria'].queryset = Categoria.objects.none()

        # Para subcategoría, si se envió 'categoria' y 'modalidad', filtramos las opciones
        if self.data.get('categoria') and self.data.get('modalidad'):
            self.fields['subcategoria'].queryset = Subcategoria.objects.filter(
                categoria_id=self.data.get('categoria'),
                modalidad=self.data.get('modalidad')
            )
        else:
            self.fields['subcategoria'].queryset = Subcategoria.objects.none()
