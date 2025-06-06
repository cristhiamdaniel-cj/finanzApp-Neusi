from django.db import models
from django.contrib.auth.models import User

class Cuenta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    TIPO_TRANSACCION = (
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    )
    MODALIDAD_CHOICES = [
        ('fijo', 'Fijo'),
        ('variable', 'Variable'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_TRANSACCION)
    modalidad = models.CharField(max_length=10, choices=MODALIDAD_CHOICES)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()} - {self.get_modalidad_display()})"


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
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.PROTECT)

    # 🚨 TEMPORALMENTE permitir null para migrar sin errores
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cuenta_origen = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='transacciones_salida', null=True)
    cuenta_destino = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='transacciones_entrada', blank=True, null=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.categoria.nombre} - {self.monto} ({self.fecha.strftime('%Y-%m-%d')})"
