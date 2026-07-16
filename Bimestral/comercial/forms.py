from django import forms

from .models import Usuario
from .models import Empresa
from .models import Vendedor
from .models import Producto
from .models import Inventario
from .models import Pedido
from .models import DetallePedido
from .models import Pago


class LoginForm(forms.Form):
    correo = forms.EmailField()
    contrasena = forms.CharField(widget=forms.PasswordInput)


class UsuarioEmpresaForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'correo',
            'contrasena',
            'telefono',
        ]


class RegistroEmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'razon_social',
            'ruc',
            'direccion',
            'sector',
            'limite_compra',
            'valor_base_sector',
        ]


class UsuarioVendedorForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'correo',
            'contrasena',
            'telefono',
        ]


class RegistroVendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = [
            'cedula',
            'direccion',
        ]


class ProductoEmpresaForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'categoria',
            'disponible',
        ]


class InventarioEmpresaForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = [
            'producto',
            'stock_actual',
            'stock_reservado',
        ]


class PedidoVendedorForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'empresa',
        ]


class DetallePedidoVendedorForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = [
            'pedido',
            'producto',
            'cantidad',
            'precio_unitario',
        ]


class PagoVendedorForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'pedido',
            'metodo_pago',
            'monto',
            'estado_pago',
        ]
class LoginForm(forms.Form):
    correo = forms.EmailField()
    contrasena = forms.CharField(widget=forms.PasswordInput)


class UsuarioEmpresaForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'correo',
            'contrasena',
            'telefono',
        ]


class RegistroEmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'razon_social',
            'ruc',
            'direccion',
            'sector',
            'limite_compra',
            'valor_base_sector',
        ]


class UsuarioVendedorForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'correo',
            'contrasena',
            'telefono',
        ]


class RegistroVendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = [
            'cedula',
            'direccion',
        ]


class ProductoEmpresaForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'categoria',
            'disponible',
        ]


class InventarioEmpresaForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = [
            'producto',
            'stock_actual',
            'stock_reservado',
        ]


class PedidoVendedorForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'empresa',
        ]


class DetallePedidoVendedorForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = [
            'pedido',
            'producto',
            'cantidad',
            'precio_unitario',
        ]


class PagoVendedorForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'pedido',
            'metodo_pago',
            'monto',
            'estado_pago',
        ]