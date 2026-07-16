from rest_framework import serializers

from .models import Usuario
from .models import Empresa
from .models import Vendedor
from .models import Producto
from .models import Inventario
from .models import Pedido
from .models import DetallePedido
from .models import Pago
from .models import Factura
from .models import Comision
from .models import Suscripcion
from .models import Calificacion
from .models import Notificacion
from .models import Tutorial


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'url',
            'id',
            'nombre',
            'correo',
            'contrasena',
            'telefono',
            'estado',
            'tipo_usuario',
        ]


class EmpresaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Empresa
        fields = [
            'url',
            'id',
            'usuario',
            'razon_social',
            'ruc',
            'direccion',
            'sector',
            'limite_compra',
            'valor_base_sector',
            'estado_validacion',
        ]


class VendedorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendedor
        fields = [
            'url',
            'id',
            'usuario',
            'cedula',
            'direccion',
            'calificacion',
            'total_ventas',
            'nivel',
            'estado_validacion',
        ]


class ProductoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'url',
            'id',
            'empresa',
            'nombre',
            'descripcion',
            'precio',
            'categoria',
            'disponible',
        ]


class InventarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inventario
        fields = [
            'url',
            'id',
            'producto',
            'stock_actual',
            'stock_reservado',
            'fecha_actualizacion',
        ]


class PedidoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'url',
            'id',
            'vendedor',
            'empresa',
            'fecha_pedido',
            'estado',
            'subtotal',
            'total',
        ]


class DetallePedidoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DetallePedido
        fields = [
            'url',
            'id',
            'pedido',
            'producto',
            'cantidad',
            'precio_unitario',
            'subtotal',
        ]


class PagoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pago
        fields = [
            'url',
            'id',
            'pedido',
            'metodo_pago',
            'monto',
            'estado_pago',
            'fecha_pago',
        ]


class FacturaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Factura
        fields = [
            'url',
            'id',
            'pedido',
            'numero_factura',
            'fecha_emision',
            'total',
        ]


class ComisionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comision
        fields = [
            'url',
            'id',
            'pedido',
            'porcentaje',
            'valor_comision',
            'fecha_calculo',
        ]


class SuscripcionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Suscripcion
        fields = [
            'url',
            'id',
            'empresa',
            'tipo',
            'valor',
            'fecha_inicio',
            'fecha_fin',
            'estado',
        ]


class CalificacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Calificacion
        fields = [
            'url',
            'id',
            'empresa',
            'vendedor',
            'puntuacion',
            'comentario',
            'fecha',
        ]


class NotificacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notificacion
        fields = [
            'url',
            'id',
            'usuario',
            'tipo',
            'mensaje',
            'leida',
            'fecha_envio',
        ]


class TutorialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tutorial
        fields = [
            'url',
            'id',
            'titulo',
            'descripcion',
            'url_contenido',
            'vendedores',
        ]