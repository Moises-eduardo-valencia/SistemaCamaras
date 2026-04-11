import base64
import io

import qrcode
from django import forms
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import reverse

from .models import Camara


# ── Acción: cambiar empresa ────────────────────────────────────────────────────

class CambiarEmpresaForm(forms.Form):
    empresa = forms.CharField(
        max_length=100,
        label='Nueva empresa',
        widget=forms.TextInput(attrs={'size': 40}),
    )


@admin.action(description='Cambiar empresa de cámaras seleccionadas')
def cambiar_empresa(modeladmin, request, queryset):
    if 'aplicar' in request.POST:
        form = CambiarEmpresaForm(request.POST)
        if form.is_valid():
            nueva_empresa = form.cleaned_data['empresa']
            total = queryset.update(empresa=nueva_empresa)
            modeladmin.message_user(
                request,
                f'Se actualizó la empresa a "{nueva_empresa}" en {total} cámara(s).',
            )
            return None
    else:
        form = CambiarEmpresaForm()

    return TemplateResponse(
        request,
        'admin/camaras/cambiar_empresa.html',
        {
            'form': form,
            'queryset': queryset,
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
            'opts': modeladmin.model._meta,
        },
    )


# ── Acción: generar etiquetas con QR ──────────────────────────────────────────

def _generar_qr_b64(url: str) -> str:
    """Genera un QR code pequeño como PNG base64."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=4,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()


@admin.action(description='Generar etiquetas QR redondas (nombre + IP)')
def generar_etiquetas_qr_redondas(modeladmin, request, queryset):
    grupos = {}
    for camara in queryset.order_by('empresa', 'nombre'):
        url = request.build_absolute_uri(
            reverse('mantenimiento_rapido', args=[camara.token])
        )
        empresa = camara.empresa
        if empresa not in grupos:
            grupos[empresa] = []
        grupos[empresa].append({
            'camara': camara,
            'url': url,
            'qr_b64': _generar_qr_b64(url),
        })

    return TemplateResponse(
        request,
        'admin/camaras/etiquetas_qr_redondas.html',
        {
            'grupos': grupos,
            'opts': modeladmin.model._meta,
        },
    )


@admin.action(description='Generar etiquetas QR por empresa')
def generar_etiquetas_qr(modeladmin, request, queryset):
    grupos = {}
    for camara in queryset.order_by('empresa', 'nombre'):
        url = request.build_absolute_uri(
            reverse('mantenimiento_rapido', args=[camara.token])
        )
        empresa = camara.empresa
        if empresa not in grupos:
            grupos[empresa] = []
        grupos[empresa].append({
            'camara': camara,
            'url': url,
            'qr_b64': _generar_qr_b64(url),
        })

    return TemplateResponse(
        request,
        'admin/camaras/etiquetas_qr.html',
        {
            'grupos': grupos,
            'opts': modeladmin.model._meta,
        },
    )


# ── ModelAdmin ─────────────────────────────────────────────────────────────────

@admin.register(Camara)
class CamaraAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'nombre', 'modelo', 'serie', 'ip', 'mac')
    list_filter = ('empresa',)
    search_fields = ('empresa', 'nombre', 'serie', 'ip', 'mac')
    actions = [cambiar_empresa, generar_etiquetas_qr, generar_etiquetas_qr_redondas]
