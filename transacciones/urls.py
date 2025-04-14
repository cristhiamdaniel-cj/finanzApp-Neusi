from django.urls import path
from . import views  # importa todas las vistas como 'views'

urlpatterns = [
    path('', views.lista_transacciones, name='lista_transacciones'),
    path('filtrar_categorias/', views.filtrar_categorias, name='filtrar_categorias'),
    path('filtrar_subcategorias/', views.filtrar_subcategorias, name='filtrar_subcategorias'),
    path('gestionar/', views.gestionar_categorias, name='gestionar_categorias'),
]
