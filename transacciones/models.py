# models.py

from django.db import models

class Categoria(models.Model):
    TIPO_TRANSACCION = (
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    )
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_TRANSACCION)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Subcategoria(models.Model):
    MODALIDAD_CHOICES = [
        ('fijo', 'Fijo'),
        ('variable', 'Variable'),
    ]
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    nombre = models.CharField(max_length=100)
    modalidad = models.CharField(max_length=10, choices=MODALIDAD_CHOICES)

    def __str__(self):
        return f"{self.nombre} - {self.get_modalidad_display()}"


class Transaccion(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.categoria.nombre} - {self.monto} el {self.fecha.strftime('%d/%m/%Y')}"
