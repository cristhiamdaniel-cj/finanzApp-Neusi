# views.py

from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import JsonResponse
from .forms import TransaccionForm
from .models import Transaccion, Categoria, Subcategoria

def lista_transacciones(request):
    if request.method == "POST":
        form = TransaccionForm(request.POST)
        if form.is_valid():
            transaccion = form.save(commit=False)
            multiplicador = int(form.cleaned_data.get('multiplicador', '1'))
            transaccion.monto = transaccion.monto * multiplicador
            transaccion.save()
            return redirect('lista_transacciones')
    else:
        form = TransaccionForm()

    transacciones = Transaccion.objects.all().order_by('-fecha')
    ingresos = Transaccion.objects.filter(categoria__tipo='ingreso').aggregate(total=Sum('monto'))['total'] or 0
    egresos = Transaccion.objects.filter(categoria__tipo='egreso').aggregate(total=Sum('monto'))['total'] or 0
    saldo = ingresos - egresos

    context = {
        'form': form,
        'transacciones': transacciones,
        'saldo': saldo,
    }
    return render(request, 'transacciones/lista_transacciones.html', context)


def filtrar_categorias(request):
    """
    Retorna las categorías que tengan el 'tipo' seleccionado
    y al menos una subcategoría con la 'modalidad' indicada.
    """
    tipo = request.GET.get('tipo')
    modalidad = request.GET.get('modalidad')
    # Filtramos categorías que sean de ese tipo
    # y que tengan al menos una subcategoría con la modalidad dada.
    categorias = Categoria.objects.filter(
        tipo=tipo,
        subcategorias__modalidad=modalidad
    ).distinct()

    data = list(categorias.values('id', 'nombre'))
    return JsonResponse({'categorias': data})


def filtrar_subcategorias(request):
    """
    Retorna las subcategorías de la categoría seleccionada
    con la modalidad indicada.
    """
    categoria_id = request.GET.get('categoria')
    modalidad = request.GET.get('modalidad')

    subcategorias = Subcategoria.objects.filter(
        categoria_id=categoria_id,
        modalidad=modalidad
    )

    data = list(subcategorias.values('id', 'nombre'))
    return JsonResponse({'subcategorias': data})
