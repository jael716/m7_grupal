from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission
from .models import Producto, Proveedor, Pedido

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)

        form_fields = ['sku', 'nombre', 'cantidad', 'categoria', 'fabricante', 'precio']
        for field in form_fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        # Obtenemos una instancia del producto pero aún no la guardamos
        producto = super().save(commit=False)
        # Verificamos si el SKU del producto ya existe
        try:
            prod_existente = Producto.objects.get(sku=producto.sku)
            # Si el producto existe, aumentamos la cantidad y guardamos
            prod_existente.cantidad += producto.cantidad
            prod_existente.save()
        except Producto.DoesNotExist:
            # Si el producto no existe, simplemente lo guardamos
            if commit:
                producto.save()
        return producto
     

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)

        form_fields = ['rut', 'nombre', 'razon_social']
        for field in form_fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class PedidoForm(forms.ModelForm):
    class Meta:
        model= Pedido
        fields = ['nombre','cantidad']
        
    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)

        form_fields = ['nombre', 'cantidad']
        for field in form_fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


 

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(label="Confirmacion contraseña", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    date = forms.DateField(widget=forms.DateInput(attrs={"class":"form-control"}))
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

class LoginForm(forms.Form):
    nombre   = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

