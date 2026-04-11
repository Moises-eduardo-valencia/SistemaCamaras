import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

# Modelo para la tabla de camaras
# empresa: nombre de la empresa a la que pertenece la camara
# nombre: nombre de la camara
# modelo: modelo de la camara
# serie: numero de serie de la camara
# ip: direccion ip de la camara
# mac: direccion mac de la camara


class Camara(models.Model):
    empresa = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    serie = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=17)

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Camara')
        verbose_name_plural = _('Camaras')
        ordering = ['-created_at']

    def __str__(self):
        return self.empresa + ' - ' + self.nombre + ' - ' + self.modelo + ' - ' + self.serie 