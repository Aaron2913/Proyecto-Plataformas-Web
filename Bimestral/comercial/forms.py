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
from .models import PedidoEmpresa
from .models import DetallePedidoEmpresa
from .models import PagoPedidoEmpresa


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
            'fecha_fundacion',
            'historia',
            'limite_compra',
            'valor_base_sector',
        ]
        widgets = {
            'fecha_fundacion': forms.DateInput(attrs={'type': 'date'}),
            'historia': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'razon_social': 'Razón social',
            'fecha_fundacion': 'Fecha de fundación',
            'historia': 'Historia de la empresa',
            'limite_compra': 'Límite de compra',
            'valor_base_sector': 'Valor base del sector',
        }


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
            'nombre_tienda',
            'ruc',
            'direccion',
            'sector',
            'fecha_apertura',
            'descripcion_tienda',
            'referencia_ubicacion',
        ]
        widgets = {
            'fecha_apertura': forms.DateInput(attrs={'type': 'date'}),
            'descripcion_tienda': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'nombre_tienda': 'Nombre de la tienda',
            'fecha_apertura': 'Fecha de apertura',
            'descripcion_tienda': 'Descripción de la tienda',
            'referencia_ubicacion': 'Referencia de ubicación',
        }


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
            if pedido.estado not in ["PENDIENTE", "CONFIRMADO"]:
                raise forms.ValidationError(
                    "El pedido ya está cerrado. Debe crear una orden nueva."
                )

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
        ]

    def clean(self):
        datos = super().clean()
        pedido = datos.get('pedido')
        monto = datos.get('monto')

        if pedido is not None:
            if pedido.estado not in ["PENDIENTE", "CONFIRMADO"]:
                raise forms.ValidationError(
                    "El pedido ya está cerrado y no puede pagarse nuevamente."
                )

            if pedido.detalles.count() == 0:
                raise forms.ValidationError(
                    "El pedido no tiene productos para pagar."
                )

            total_pedido = pedido.obtener_total()

            if monto is not None and monto != total_pedido:
                raise forms.ValidationError(
                    "El monto debe ser igual al total del pedido: $%s." % total_pedido
                )

        return datos


class PedidoEmpresaTenderoForm(forms.ModelForm):
    class Meta:
        model = PedidoEmpresa
        fields = [
            'empresa',
        ]
        labels = {
            'empresa': 'Empresa proveedora',
        }


class DetallePedidoEmpresaTenderoForm(forms.ModelForm):
    class Meta:
        model = DetallePedidoEmpresa
        fields = [
            'pedido',
            'producto',
            'cantidad',
        ]
        labels = {
            'pedido': 'Pedido abierto',
            'producto': 'Producto de la empresa',
            'cantidad': 'Cantidad solicitada',
        }

    def clean(self):
        datos = super().clean()
        pedido = datos.get('pedido')
        producto = datos.get('producto')
        cantidad = datos.get('cantidad')

        if pedido is not None and producto is not None:
            if pedido.estado not in ["PENDIENTE", "CONFIRMADO"]:
                raise forms.ValidationError(
                    "La orden ya está cerrada. Debe crear una compra nueva."
                )

            if pedido.empresa != producto.empresa:
                raise forms.ValidationError(
                    "El producto no pertenece a la empresa seleccionada en la orden."
                )

            if not hasattr(producto, 'inventario'):
                raise forms.ValidationError(
                    "El producto no tiene inventario registrado en la empresa."
                )

            if cantidad is not None and cantidad > producto.inventario.obtener_stock_disponible():
                raise forms.ValidationError(
                    "La cantidad supera el stock disponible de la empresa."
                )

        return datos


class PagoPedidoEmpresaTenderoForm(forms.ModelForm):
    class Meta:
        model = PagoPedidoEmpresa
        fields = [
            'pedido',
            'metodo_pago',
            'monto',
        ]
        labels = {
            'pedido': 'Pedido a pagar',
            'metodo_pago': 'Método de pago',
            'monto': 'Monto exacto',
        }

    def clean(self):
        datos = super().clean()
        pedido = datos.get('pedido')
        monto = datos.get('monto')

        if pedido is not None:
            if pedido.estado not in ["PENDIENTE", "CONFIRMADO"]:
                raise forms.ValidationError(
                    "La orden ya está cerrada y no puede pagarse nuevamente."
                )

            if pedido.detalles.count() == 0:
                raise forms.ValidationError(
                    "La orden no tiene productos para pagar."
                )

            total_pedido = pedido.obtener_total()

            if monto is not None and monto != total_pedido:
                raise forms.ValidationError(
                    "El monto debe ser igual al total de la orden: $%s." % total_pedido
                )

        return datos
