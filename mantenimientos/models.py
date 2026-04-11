from datetime import date, timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _

from camaras.models import Camara


def proxima_fecha_habil(desde: date) -> date:
    """Retorna la fecha desde + 30 días, saltando sábado y domingo."""
    proxima = desde + timedelta(days=30)
    if proxima.weekday() == 5:    # sábado → lunes
        proxima += timedelta(days=2)
    elif proxima.weekday() == 6:  # domingo → lunes
        proxima += timedelta(days=1)
    return proxima


class Mantenimiento(models.Model):
    camara = models.ForeignKey(
        Camara,
        on_delete=models.CASCADE,
        verbose_name=_('Cámara'),
        related_name='mantenimientos',
    )
    limpieza_lente = models.BooleanField(
        default=False,
        verbose_name=_('Limpieza de lente'),
    )
    limpieza_interior = models.BooleanField(
        default=False,
        verbose_name=_('Limpieza interior'),
    )
    verificacion_conector = models.BooleanField(
        default=False,
        verbose_name=_('Verificación de conector'),
    )
    verificacion_alimentacion = models.BooleanField(
        default=False,
        verbose_name=_('Verificación de alimentación'),
    )
    fecha_mantenimiento = models.DateField(
        verbose_name=_('Fecha de mantenimiento'),
    )
    proxima_fecha = models.DateField(
        verbose_name=_('Próxima fecha'),
    )
    observaciones = models.TextField(
        blank=True,
        verbose_name=_('Observaciones'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_mantenimiento']
        verbose_name = _('Mantenimiento')
        verbose_name_plural = _('Mantenimientos')

    def __str__(self) -> str:
        return f"{self.camara.nombre} - {self.fecha_mantenimiento}"


class DestinatarioReporte(models.Model):
    empresa = models.CharField(max_length=100, verbose_name=_('Empresa'))
    email = models.EmailField(verbose_name=_('Correo electrónico'))
    activo = models.BooleanField(default=True, verbose_name=_('Activo'))

    class Meta:
        verbose_name = _('Destinatario de reporte')
        verbose_name_plural = _('Destinatarios de reportes')
        ordering = ['empresa', 'email']
        unique_together = [('empresa', 'email')]

    def __str__(self) -> str:
        return f"{self.empresa} — {self.email}"
