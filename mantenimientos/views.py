from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from camaras.models import Camara
from .forms import MantenimientoForm, DestinatarioReporteForm
from .models import Mantenimiento, DestinatarioReporte, proxima_fecha_habil


# ── Mantenimientos ────────────────────────────────────────────────────────────

@login_required
def lista_mantenimientos(request):
    empresas = (
        Mantenimiento.objects
        .select_related('camara')
        .values_list('camara__empresa', flat=True)
        .distinct()
        .order_by('camara__empresa')
    )
    empresa_seleccionada = request.GET.get('empresa', '').strip()

    mantenimientos = Mantenimiento.objects.select_related('camara').all()
    if empresa_seleccionada:
        mantenimientos = mantenimientos.filter(camara__empresa=empresa_seleccionada)

    total = Mantenimiento.objects.count()

    return render(request, 'mantenimientos/lista_mantenimientos.html', {
        'mantenimientos': mantenimientos,
        'empresas': empresas,
        'empresa_seleccionada': empresa_seleccionada,
        'total': total,
    })


@login_required
def registrar_mantenimiento(request):
    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mantenimiento registrado correctamente.')
            return redirect('lista_mantenimientos')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = MantenimientoForm()
    return render(request, 'mantenimientos/registrar_mantenimiento.html', {'form': form})


@login_required
def editar_mantenimiento(request, pk: int):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    if request.method == 'POST':
        form = MantenimientoForm(request.POST, instance=mantenimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mantenimiento actualizado correctamente.')
            return redirect('lista_mantenimientos')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = MantenimientoForm(instance=mantenimiento)
    return render(request, 'mantenimientos/editar_mantenimiento.html', {
        'form': form,
        'mant': mantenimiento,
    })


@login_required
def eliminar_mantenimiento(request, pk: int):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    if request.method == 'POST':
        mantenimiento.delete()
        messages.success(request, 'Mantenimiento eliminado correctamente.')
        return redirect('lista_mantenimientos')
    return render(request, 'mantenimientos/eliminar_mantenimiento.html', {
        'mant': mantenimiento,
    })


# ── Mantenimiento rápido (QR / NFC) ──────────────────────────────────────────

def mantenimiento_rapido(request, token):
    """Vista pública (sin login). Se accede via QR o NFC."""
    camara = get_object_or_404(Camara, token=token)

    hoy = date.today()
    proxima = proxima_fecha_habil(hoy)

    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mantenimiento_rapido_exito', token=token)
    else:
        form = MantenimientoForm(initial={
            'camara': camara,
            'fecha_mantenimiento': hoy,
            'proxima_fecha': proxima,
        })
        # Bloquear el campo cámara para que no se pueda cambiar
        form.fields['camara'].widget.attrs['disabled'] = True
        form.fields['camara'].required = False

    return render(request, 'mantenimientos/mantenimiento_rapido.html', {
        'camara': camara,
        'form': form,
        'hoy': hoy,
        'proxima': proxima,
    })


def mantenimiento_rapido_exito(request, token):
    camara = get_object_or_404(Camara, token=token)
    return render(request, 'mantenimientos/mantenimiento_rapido_exito.html', {
        'camara': camara,
    })


# ── Destinatarios de reportes ─────────────────────────────────────────────────

@login_required
def lista_destinatarios(request):
    empresas = (DestinatarioReporte.objects
                .values_list('empresa', flat=True)
                .distinct()
                .order_by('empresa'))
    destinatarios = DestinatarioReporte.objects.all()
    return render(request, 'mantenimientos/lista_destinatarios.html', {
        'destinatarios': destinatarios,
        'empresas': empresas,
    })


@login_required
def agregar_destinatario(request):
    if request.method == 'POST':
        form = DestinatarioReporteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Destinatario agregado.')
            return redirect('lista_destinatarios')
    else:
        form = DestinatarioReporteForm()
    return render(request, 'mantenimientos/form_destinatario.html', {'form': form})


@login_required
def eliminar_destinatario(request, pk: int):
    dest = get_object_or_404(DestinatarioReporte, pk=pk)
    if request.method == 'POST':
        dest.delete()
        messages.success(request, f'Destinatario {dest.email} eliminado.')
        return redirect('lista_destinatarios')
    return render(request, 'mantenimientos/eliminar_destinatario.html', {'dest': dest})


@login_required
def toggle_destinatario(request, pk: int):
    dest = get_object_or_404(DestinatarioReporte, pk=pk)
    if request.method == 'POST':
        dest.activo = not dest.activo
        dest.save()
    return redirect('lista_destinatarios')
