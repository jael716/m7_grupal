from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.
class Proveedor(models.Model):
    rut = models.CharField(max_length=9)
    nombre = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100)

    
class Producto(models.Model):
    sku = models.IntegerField()
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    categoria = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    precio = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor,null=True, on_delete=models.SET_NULL)



class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('EP', 'En Preparacion'),
        ('ED', 'En Despacho'),
        ('E', 'Entregado'),
    ]
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, default='P')
    cancelado = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('S', 'Staff'),
        ('C', 'Cliente'),
    ]
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default='C')
    
    def can_alter_pedido_status(self, pedido):
        # Check if the user is a staff member or if they placed the order
        return self.is_staff or (self.user_type == 'C' and pedido.user == self)

    def can_cancel_pedido(self, pedido):
        # Check if the user is a staff member or if they placed the order
        # and the pedido is not already cancelled
        return self.is_staff or (self.user_type == 'C' and not pedido.cancelado)

    def get_user_type_display(self):
        # Get the display value of the user_type field
        return dict(self.USER_TYPE_CHOICES).get(self.user_type, '')

    def __str__(self):
        return self.username
