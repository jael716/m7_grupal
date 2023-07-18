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


@login_required
def producto(request):
    form = ProductoForm()
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/producto')
    context = {'form': form}
    return render(request, 'producto.html', context=context)


@login_required
def pedido(request):
   
    form = PedidoForm()

    if request.method == "POST":
        form = PedidoForm(request.POST)
 
        if form.is_valid():

            pedido = Pedido()
            pedido.nombre = form.cleaned_data['nombre']
            print(pedido.nombre)

            pedido.cantidad = form.cleaned_data['cantidad']
            print(pedido.cantidad)

            form.save()
            
        else:
            print("Datos invalidos")
        return redirect('/vistapedidos')
    context = {'form': form}

    return render(request, 'pedido.html', context=context)


@login_required
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
    return render(request, 'register_user.html', context)

    
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