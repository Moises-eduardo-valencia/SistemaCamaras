from django import forms

from camaras.models import Camara
from .models import Mantenimiento, DestinatarioReporte


class CamaraChoiceField(forms.ModelChoiceField):
    """ModelChoiceField que muestra las cámaras como 'empresa — nombre (serie)'."""

    def label_from_instance(self, obj: Camara) -> str:
        return f"{obj.empresa} — {obj.nombre} ({obj.serie})"


class MantenimientoForm(forms.ModelForm):
    camara = CamaraChoiceField(
        queryset=Camara.objects.all().order_by('empresa', 'nombre'),
        label='Cámara',
    )

    class Meta:
        model = Mantenimiento
        fields = [
            'camara',
            'limpieza_lente',
            'limpieza_interior',
            'verificacion_conector',
            'verificacion_alimentacion',
            'fecha_mantenimiento',
            'proxima_fecha',
            'observaciones',
        ]
        widgets = {
            'fecha_mantenimiento': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
            'proxima_fecha': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }


class DestinatarioReporteForm(forms.ModelForm):
    class Meta:
        model = DestinatarioReporte
        fields = ['empresa', 'email', 'activo']
