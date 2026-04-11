from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CamaraForm
from .models import Camara


@login_required
def registrar_camara(request):
    if request.method == 'POST':
        form = CamaraForm(request.POST)
        if form.is_valid():
            camara = form.save()
            messages.success(
                request,
                f'Cámara "{camara.nombre}" registrada exitosamente.',
            )
            return redirect('lista_camaras')
        else:
            messages.error(
                request,
                'Por favor corrige los errores del formulario.',
            )
    else:
        form = CamaraForm()

    return render(request, 'registrar_camara.html', {'form': form})


@login_required
def lista_camaras(request):
    empresas = (
        Camara.objects
        .values_list('empresa', flat=True)
        .distinct()
        .order_by('empresa')
    )
    empresa_seleccionada = request.GET.get('empresa', '').strip()

    camaras = Camara.objects.all()
    if empresa_seleccionada:
        camaras = camaras.filter(empresa=empresa_seleccionada)

    total = Camara.objects.count()

    return render(request, 'lista_camaras.html', {
        'camaras': camaras,
        'empresas': empresas,
        'empresa_seleccionada': empresa_seleccionada,
        'total': total,
    })


@login_required
def editar_camara(request, pk: int):
    camara = get_object_or_404(Camara, pk=pk)

    if request.method == 'POST':
        form = CamaraForm(request.POST, instance=camara)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Cámara "{camara.nombre}" actualizada exitosamente.',
            )
            return redirect('lista_camaras')
        else:
            messages.error(
                request,
                'Por favor corrige los errores del formulario.',
            )
    else:
        form = CamaraForm(instance=camara)

    return render(request, 'editar_camara.html', {'form': form, 'camara': camara})


@login_required
def eliminar_camara(request, pk: int):
    camara = get_object_or_404(Camara, pk=pk)

    if request.method == 'POST':
        nombre = camara.nombre
        camara.delete()
        messages.success(
            request,
            f'Cámara "{nombre}" eliminada exitosamente.',
        )
        return redirect('lista_camaras')

    return render(request, 'eliminar_camara.html', {'camara': camara})
