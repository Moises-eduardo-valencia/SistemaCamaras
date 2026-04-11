"""
Lógica central de envío de reportes.
Llamada tanto por los management commands como por el scheduler automático.
"""

from datetime import date

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

import logging

logger = logging.getLogger(__name__)


def enviar_reporte_inventario(empresa_filtro=None):
    """
    Envía el reporte de inventario de cámaras a los destinatarios activos.
    Retorna (enviados, errores).
    """
    from camaras.models import Camara
    from mantenimientos.models import DestinatarioReporte

    mes_actual = timezone.now().strftime('%B %Y')

    empresas = (Camara.objects
                .values_list('empresa', flat=True)
                .distinct()
                .order_by('empresa'))

    if empresa_filtro:
        empresas = [e for e in empresas if e == empresa_filtro]

    enviados, errores = 0, 0

    for empresa in empresas:
        destinatarios = list(
            DestinatarioReporte.objects
            .filter(empresa=empresa, activo=True)
            .values_list('email', flat=True)
        )

        if not destinatarios:
            logger.info('Sin destinatarios activos para: %s', empresa)
            continue

        camaras = Camara.objects.filter(empresa=empresa).order_by('nombre')

        html = render_to_string('mantenimientos/email/reporte_inventario.html', {
            'empresa': empresa,
            'camaras': camaras,
            'mes': mes_actual,
            'total': camaras.count(),
        })

        msg = EmailMultiAlternatives(
            subject=f'[SistemaCamaras] Inventario {empresa} — {mes_actual}',
            body=f'Inventario {empresa} — {mes_actual}. Total: {camaras.count()} cámara(s).',
            to=destinatarios,
        )
        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
            enviados += 1
            logger.info('Reporte inventario enviado: %s → %s', empresa, destinatarios)
        except Exception as exc:
            errores += 1
            logger.error('Error al enviar inventario %s: %s', empresa, exc)

    return enviados, errores


def enviar_reporte_mantenimientos(empresa_filtro=None, año=None, mes=None):
    """
    Envía el reporte de mantenimientos del mes indicado (por defecto el mes anterior).
    Retorna (enviados, errores).
    """
    from camaras.models import Camara
    from mantenimientos.models import DestinatarioReporte, Mantenimiento

    hoy = timezone.now().date()

    if año and mes:
        fecha_inicio = date(año, mes, 1)
    else:
        # Mes anterior por defecto (se envía el 1ro del mes nuevo)
        if hoy.month == 1:
            fecha_inicio = date(hoy.year - 1, 12, 1)
        else:
            fecha_inicio = date(hoy.year, hoy.month - 1, 1)

    if fecha_inicio.month == 12:
        fecha_fin = date(fecha_inicio.year + 1, 1, 1)
    else:
        fecha_fin = date(fecha_inicio.year, fecha_inicio.month + 1, 1)

    mes_label = fecha_inicio.strftime('%B %Y')

    empresas = (Camara.objects
                .values_list('empresa', flat=True)
                .distinct()
                .order_by('empresa'))

    if empresa_filtro:
        empresas = [e for e in empresas if e == empresa_filtro]

    enviados, errores = 0, 0

    for empresa in empresas:
        destinatarios = list(
            DestinatarioReporte.objects
            .filter(empresa=empresa, activo=True)
            .values_list('email', flat=True)
        )

        if not destinatarios:
            logger.info('Sin destinatarios activos para: %s', empresa)
            continue

        mantenimientos = (Mantenimiento.objects
                          .filter(
                              camara__empresa=empresa,
                              fecha_mantenimiento__gte=fecha_inicio,
                              fecha_mantenimiento__lt=fecha_fin,
                          )
                          .select_related('camara')
                          .order_by('fecha_mantenimiento', 'camara__nombre'))

        html = render_to_string('mantenimientos/email/reporte_mantenimientos.html', {
            'empresa': empresa,
            'mantenimientos': mantenimientos,
            'mes': mes_label,
            'total': mantenimientos.count(),
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
        })

        msg = EmailMultiAlternatives(
            subject=f'[SistemaCamaras] Mantenimientos {empresa} — {mes_label}',
            body=f'Mantenimientos {empresa} — {mes_label}. Total: {mantenimientos.count()}.',
            to=destinatarios,
        )
        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
            enviados += 1
            logger.info('Reporte mantenimientos enviado: %s → %s', empresa, destinatarios)
        except Exception as exc:
            errores += 1
            logger.error('Error al enviar mantenimientos %s: %s', empresa, exc)

    return enviados, errores
