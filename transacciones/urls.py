from django.urls import path
from .views import lista_transacciones, filtrar_categorias, filtrar_subcategorias

urlpatterns = [
    path('', lista_transacciones, name='lista_transacciones'),
    path('filtrar_categorias/', filtrar_categorias, name='filtrar_categorias'),
    path('filtrar_subcategorias/', filtrar_subcategorias, name='filtrar_subcategorias'),
]
