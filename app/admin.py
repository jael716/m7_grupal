from django.contrib import admin
from .models import Producto, Proveedor, Pedido, User
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Proveedor)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email')
    list_filter = ('is_staff', 'is_superuser')

#admin.site.unregister(User)
admin.site.register(User, UserAdmin)


