from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import JsonResponse
from .forms import TransaccionForm
from .models import Transaccion, Categoria, Subcategoria
from django.contrib import messages

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
    tipo = request.GET.get('tipo')
    modalidad = request.GET.get('modalidad')
    categorias = Categoria.objects.filter(
        tipo=tipo,
        subcategorias__modalidad=modalidad
    ).distinct()
    data = list(categorias.values('id', 'nombre'))
    return JsonResponse({'categorias': data})

def filtrar_subcategorias(request):
    categoria_id = request.GET.get('categoria')
    modalidad = request.GET.get('modalidad')
    subcategorias = Subcategoria.objects.filter(
        categoria_id=categoria_id,
        modalidad=modalidad
    )
    data = list(subcategorias.values('id', 'nombre'))
    return JsonResponse({'subcategorias': data})

# NUEVA VISTA: gestión de categorías y subcategorías
def gestionar_categorias(request):
    tipos = ['ingreso', 'egreso']
    modalidades = ['fijo', 'variable']
    selected_tipo = request.GET.get('tipo') or request.POST.get('tipo')
    selected_modalidad = request.GET.get('modalidad') or request.POST.get('modalidad')
    categorias = Categoria.objects.filter(tipo=selected_tipo) if selected_tipo else []

    selected_categoria_id = request.POST.get('categoria_id')
    subcategorias = Subcategoria.objects.filter(categoria_id=selected_categoria_id) if selected_categoria_id else []

    if request.method == "POST":
        if 'crear_categoria' in request.POST:
            nombre_categoria = request.POST.get('nombre_categoria')
            if selected_tipo and selected_modalidad:
                Categoria.objects.create(
                    nombre=nombre_categoria,
                    tipo=selected_tipo,
                    modalidad=selected_modalidad
                )
                messages.success(request, f"Categoría '{nombre_categoria}' creada correctamente.")
                return redirect(f"{request.path}?tipo={selected_tipo}&modalidad={selected_modalidad}")

        elif 'crear_subcategoria' in request.POST:
            nombre_subcategoria = request.POST.get('nombre_subcategoria')
            if selected_categoria_id and selected_modalidad:
                Subcategoria.objects.create(
                    nombre=nombre_subcategoria,
                    modalidad=selected_modalidad,
                    categoria_id=selected_categoria_id
                )
                messages.success(request, f"Subcategoría '{nombre_subcategoria}' creada correctamente.")
                return redirect(f"{request.path}?tipo={selected_tipo}&modalidad={selected_modalidad}&categoria_id={selected_categoria_id}")

    context = {
        'tipos': tipos,
        'modalidades': modalidades,
        'selected_tipo': selected_tipo,
        'selected_modalidad': selected_modalidad,
        'categorias': categorias,
        'selected_categoria_id': selected_categoria_id,
        'subcategorias': subcategorias,
    }
    return render(request, 'transacciones/gestionar_categorias.html', context)
