from django import forms

from .models import Usuario
from .models import Empresa
from .models import Vendedor
from .models import Tienda
from .models import Producto
from .models import Inventario
from .models import ProductoTienda
from .models import Pedido
from .models import DetallePedido
from .models import Pago


class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo")
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


class UsuarioEmpresaForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'correo',
            'contrasena',
            'telefono',
        ]
        widgets = {
            'contrasena': forms.PasswordInput(),
        }


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


class UsuarioTenderoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'correo',
            'contrasena',
            'telefono',
        ]
        widgets = {
            'contrasena': forms.PasswordInput(),
        }


class RegistroTiendaForm(forms.ModelForm):
    class Meta:
        model = Tienda
        fields = [
            'empresa',
            'nombre_tienda',
            'ruc',
            'direccion',
            'sector',
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
        widgets = {
            'contrasena': forms.PasswordInput(),
        }


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


class ProductoTiendaForm(forms.ModelForm):
    class Meta:
        model = ProductoTienda
        fields = [
            'producto',
            'precio_venta',
            'stock_actual',
            'disponible',
        ]


class PedidoVendedorForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'tienda',
        ]


class DetallePedidoVendedorForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = [
            'pedido',
            'producto_tienda',
            'cantidad',
        ]

    def clean(self):
        datos = super().clean()
        pedido = datos.get('pedido')
        producto_tienda = datos.get('producto_tienda')

        if pedido is not None and producto_tienda is not None:
            if pedido.tienda != producto_tienda.tienda:
                raise forms.ValidationError(
                    "El producto seleccionado no pertenece a la tienda del pedido."
                )

            if datos.get('cantidad') is not None:
                if datos.get('cantidad') > producto_tienda.obtener_stock_disponible():
                    raise forms.ValidationError(
                        "La cantidad supera el stock disponible en la tienda."
                    )

        return datos


class PagoVendedorForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'pedido',
            'metodo_pago',
            'monto',
            'estado_pago',
        ]
