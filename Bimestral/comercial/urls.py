from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

from . import views

from .views import UsuarioViewSet
from .views import EmpresaViewSet
from .views import VendedorViewSet
from .views import TiendaViewSet
from .views import ProductoViewSet
from .views import InventarioViewSet
from .views import ProductoTiendaViewSet
from .views import PedidoViewSet
from .views import DetallePedidoViewSet
from .views import PagoViewSet
from .views import PedidoEmpresaViewSet
from .views import DetallePedidoEmpresaViewSet
from .views import PagoPedidoEmpresaViewSet
from .views import FacturaViewSet
from .views import ComisionViewSet
from .views import SuscripcionViewSet
from .views import CalificacionViewSet
from .views import NotificacionViewSet
from .views import TutorialViewSet


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'empresas', EmpresaViewSet)
router.register(r'vendedores', VendedorViewSet)
router.register(r'tiendas', TiendaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'inventarios', InventarioViewSet)
router.register(r'productos-tienda', ProductoTiendaViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'pedidos-empresa', PedidoEmpresaViewSet)
router.register(r'detalles-pedido-empresa', DetallePedidoEmpresaViewSet)
router.register(r'pagos-pedido-empresa', PagoPedidoEmpresaViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'comisiones', ComisionViewSet)
router.register(r'suscripciones', SuscripcionViewSet)
router.register(r'calificaciones', CalificacionViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'tutoriales', TutorialViewSet)


urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('login/', views.login_usuario, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),

    path('registro/empresa/', views.registro_empresa, name='registro_empresa'),
    path('registro/tendero/', views.registro_tendero, name='registro_tendero'),
    path('registro/vendedor/', views.registro_vendedor, name='registro_vendedor'),

    path('empresa/inicio/', views.inicio_empresa, name='inicio_empresa'),
    path('empresa/productos/', views.productos_empresa, name='productos_empresa'),
    path('empresa/productos/crear/', views.crear_producto_empresa, name='crear_producto_empresa'),
    path('empresa/inventario/', views.inventario_empresa, name='inventario_empresa'),
    path('empresa/inventario/crear/', views.crear_inventario_empresa, name='crear_inventario_empresa'),
    path('empresa/tiendas/', views.tiendas_empresa, name='tiendas_empresa'),
    path('empresa/pedidos/', views.pedidos_empresa, name='pedidos_empresa'),
    path('empresa/pedidos/<int:pedido_id>/confirmar/', views.confirmar_pedido_empresa, name='confirmar_pedido_empresa'),
    path('empresa/pedidos/<int:pedido_id>/preparar/', views.preparar_pedido_empresa, name='preparar_pedido_empresa'),
    path('empresa/pedidos/<int:pedido_id>/entregar/', views.entregar_pedido_empresa, name='entregar_pedido_empresa'),

    path('tendero/inicio/', views.inicio_tendero, name='inicio_tendero'),
    path('tendero/productos/', views.productos_tendero, name='productos_tendero'),
    path('tendero/productos/crear/', views.crear_producto_tendero, name='crear_producto_tendero'),
    path('tendero/catalogo-empresas/', views.catalogo_empresas_tendero, name='catalogo_empresas_tendero'),
    path('tendero/compras/', views.pedidos_empresa_tendero, name='pedidos_empresa_tendero'),
    path('tendero/compras/crear/', views.crear_pedido_empresa_tendero, name='crear_pedido_empresa_tendero'),
    path('tendero/compras/detalle/crear/', views.crear_detalle_empresa_tendero, name='crear_detalle_empresa_tendero'),
    path('tendero/compras/<int:pedido_id>/detalle/', views.detalle_pedido_empresa_tendero, name='detalle_pedido_empresa_tendero'),
    path('tendero/compras/<int:pedido_id>/cancelar/', views.cancelar_pedido_empresa_tendero, name='cancelar_pedido_empresa_tendero'),
    path('tendero/pagos-empresa/', views.pagos_empresa_tendero, name='pagos_empresa_tendero'),
    path('tendero/pagos-empresa/crear/', views.crear_pago_empresa_tendero, name='crear_pago_empresa_tendero'),
    path('tendero/pedidos/', views.pedidos_tendero, name='pedidos_tendero'),
    path('tendero/pedidos/<int:pedido_id>/confirmar/', views.confirmar_pedido_tendero, name='confirmar_pedido_tendero'),
    path('tendero/pedidos/<int:pedido_id>/preparar/', views.preparar_pedido_tendero, name='preparar_pedido_tendero'),
    path('tendero/pedidos/<int:pedido_id>/entregar/', views.entregar_pedido_tendero, name='entregar_pedido_tendero'),

    path('vendedor/inicio/', views.inicio_vendedor, name='inicio_vendedor'),
    path('vendedor/catalogo/', views.catalogo_vendedor, name='catalogo_vendedor'),
    path('vendedor/pedidos/', views.pedidos_vendedor, name='pedidos_vendedor'),
    path('pedidos/<int:pedido_id>/detalle/', views.detalle_pedido, name='detalle_pedido'),
    path('pedidos-empresa/<int:pedido_id>/detalle/', views.detalle_pedido_empresa_tendero, name='detalle_pedido_empresa'),
    path('vendedor/pedidos/crear/', views.crear_pedido_vendedor, name='crear_pedido_vendedor'),
    path('vendedor/pedidos/<int:pedido_id>/cancelar/', views.cancelar_pedido_vendedor, name='cancelar_pedido_vendedor'),
    path('vendedor/detalle/crear/', views.crear_detalle_vendedor, name='crear_detalle_vendedor'),
    path('vendedor/pagos/', views.pagos_vendedor, name='pagos_vendedor'),
    path('vendedor/pagos/crear/', views.crear_pago_vendedor, name='crear_pago_vendedor'),
    path('vendedor/tutoriales/', views.tutoriales_vendedor, name='tutoriales_vendedor'),

    path('resumen/', views.resumen, name='resumen'),
    path('api/', include(router.urls)),
]
