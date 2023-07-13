from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, ProductoForm, ProveedorForm, PedidoForm
from .models import Producto, Proveedor, Pedido
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse



# Create your views here.

def welcome(request):
    return render(request, "home.html")


@login_required
def proveedor(request):
    form = ProveedorForm()
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            print(form)
            proveedor = Proveedor()
            proveedor.rut = form.cleaned_data['rut']
            proveedor.nombre = form.cleaned_data['nombre']
            proveedor.razon_social = form.cleaned_data['razon_social']
            form.save()
        else:
            print("Datos invalidos")
        return redirect('/proveedor')
    context = {'form': form}

    return render(request, 'proveedor.html', context=context)


"""@login_required
def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']
            permissions = form.cleaned_data['permissions']
            username = form.cleaned_data['username']
            user.groups.add(group)
            user.user_permissions.set(permissions)
            messages.success(request, f'Usuario {username} creado exitosamente!!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'register_user.html', context)"""

#----------------------------------------------------------------

@login_required
def pedido(request):
    form = PedidoForm()
    productos = Producto.objects.all()

    if request.method == "POST":
        form = PedidoForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            cantidad = form.cleaned_data['cantidad']

            try:
                producto = Producto.objects.get(nombre=nombre)
            except Producto.DoesNotExist:
                messages.warning(request, f"No existe el producto {nombre}.")
                return redirect('/pedido')

            if cantidad > producto.cantidad:
                messages.warning(request, f"No hay suficiente cantidad de {nombre} disponible.")
                return redirect('/pedido')

            pedido = Pedido(nombre=nombre, cantidad=cantidad)
            pedido.save()

            producto.cantidad -= cantidad
            producto.save()

            messages.success(request, "Pedido realizado correctamente.")
            return redirect('vistapedidos')

    context = {'form': form, 'productos': productos}
    return render(request, 'pedido.html', context=context)



def pedido_list(request):
    pedidos = Pedido.objects.all()
    return render(request, 'vista_pedido.html', {'pedidos':pedidos})



def eliminar_pedido(request, id):
    
    pedidos = Pedido.objects.get(pk=id)
    if pedidos.estado=="P":
         if request.method == "POST":
             pedidos.delete()
             return redirect('vistapedidos')
    else:
        return HttpResponse("No puedes eliminar pedidos que no estén pendientes.")
    return render(request, 'eliminar_pedido.html', {'pedidos': pedidos})


def modificar_pedido(request, id):
    pedido = Pedido.objects.get(pk=id)
    form = PedidoForm(instance=pedido)
    if request.method =="POST":
        form = PedidoForm(request.POST, instance=pedido)
        form.save()
        return redirect('vistapedidos')
    else:
        return render(request, 'modificar_pedido.html', {'form':form})
    
#---------------------------------------------------------------
@login_required
def producto(request):
    form = ProductoForm()
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vistaproductos')
    context = {'form': form}
    return render(request, 'producto.html', context=context)


def producto_list(request):
    productos = Producto.objects.all()
    return render(request, 'vista_producto.html', {'productos':productos})


def eliminar_producto(request, id):
    productos = Producto.objects.get(pk=id)
    if request.method == "POST":
             productos.delete()
             return redirect('vistaproductos')
    return render(request, 'eliminar_pedido.html', {'productos': productos})


def modificar_producto(request, id):
    productos = Producto.objects.get(pk=id)
    form = ProductoForm(instance=productos)
    if request.method =="POST":
        form = PedidoForm(request.POST, instance=productos)
        form.save()
        return redirect('vistaproductos')
    else:
        return render(request, 'modificar_producto.html', {'form':form})

#----------------------------------------------------------
