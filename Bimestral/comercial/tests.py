from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .forms import (
    DetallePedidoVendedorForm,
    PagoVendedorForm,
    DetallePedidoEmpresaTenderoForm,
    PagoPedidoEmpresaTenderoForm,
)
from .models import (
    DetallePedido,
    Empresa,
    Inventario,
    Pedido,
    PedidoEmpresa,
    DetallePedidoEmpresa,
    PagoPedidoEmpresa,
    Producto,
    ProductoTienda,
    Tienda,
    Usuario,
    Vendedor,
)


class FlujoPedidoPagadoTests(TestCase):
    def setUp(self):
        usuario_empresa = Usuario.objects.create(
            nombre="Empresa de prueba",
            correo="empresa@prueba.com",
            contrasena="1234",
            telefono="0990000001",
            tipo_usuario="EMPRESA",
        )
        self.empresa = Empresa.objects.create(
            usuario=usuario_empresa,
            razon_social="Proveedor Uno",
            ruc="1100000000001",
            direccion="Loja",
            sector="Centro",
        )

        usuario_tendero = Usuario.objects.create(
            nombre="Tendero de prueba",
            correo="tendero@prueba.com",
            contrasena="1234",
            telefono="0990000002",
            tipo_usuario="TENDERO",
        )
        self.tienda = Tienda.objects.create(
            usuario=usuario_tendero,
            nombre_tienda="Tienda Uno",
            ruc="1100000000002",
            direccion="Loja",
            sector="Centro",
            estado_validacion="APROBADA",
        )

        usuario_vendedor = Usuario.objects.create(
            nombre="Delivery de prueba",
            correo="delivery@prueba.com",
            contrasena="1234",
            telefono="0990000003",
            tipo_usuario="VENDEDOR",
        )
        self.vendedor = Vendedor.objects.create(
            usuario=usuario_vendedor,
            cedula="1100000003",
            direccion="Loja",
            estado_validacion="APROBADO",
        )

        self.producto = Producto.objects.create(
            empresa=self.empresa,
            nombre="Producto de prueba",
            descripcion="Producto para validar el flujo",
            precio=Decimal("2.00"),
            categoria="Pruebas",
            disponible=True,
        )
        self.producto_tienda = ProductoTienda.objects.create(
            tienda=self.tienda,
            producto=self.producto,
            precio_venta=Decimal("2.00"),
            stock_actual=200,
            stock_reservado=0,
            disponible=True,
        )

    def crear_pedido_con_cantidad(self, cantidad):
        pedido = Pedido.objects.create(
            vendedor=self.vendedor,
            tienda=self.tienda,
        )
        detalle = DetallePedido(
            pedido=pedido,
            producto_tienda=self.producto_tienda,
            cantidad=cantidad,
        )
        detalle.registrar_detalle_con_reserva()
        pedido.refresh_from_db()
        return pedido

    def pagar_pedido(self, pedido):
        formulario = PagoVendedorForm(
            data={
                "pedido": pedido.id,
                "metodo_pago": "EFECTIVO",
                "monto": str(pedido.total),
            }
        )
        formulario = self.vendedor.configurar_formulario_pago(formulario)
        self.assertTrue(formulario.is_valid(), formulario.errors)
        self.vendedor.registrar_pago(formulario)
        pedido.refresh_from_db()

    def test_pagar_cierra_la_orden_y_descuenta_stock(self):
        pedido = self.crear_pedido_con_cantidad(50)
        self.pagar_pedido(pedido)

        self.producto_tienda.refresh_from_db()
        self.assertEqual(pedido.estado, "PAGADO")
        self.assertEqual(pedido.total, Decimal("100.00"))
        self.assertEqual(self.producto_tienda.stock_actual, 150)
        self.assertEqual(self.producto_tienda.stock_reservado, 0)
        self.assertEqual(pedido.pago.estado_pago, "APROBADO")

    def test_no_permite_agregar_producto_a_pedido_pagado(self):
        pedido = self.crear_pedido_con_cantidad(50)
        self.pagar_pedido(pedido)

        detalle_nuevo = DetallePedido(
            pedido=pedido,
            producto_tienda=self.producto_tienda,
            cantidad=10,
        )

        with self.assertRaisesMessage(ValueError, "pedido ya está cerrado"):
            detalle_nuevo.registrar_detalle_con_reserva()

        self.assertEqual(pedido.detalles.count(), 1)

    def test_nueva_compra_del_mismo_producto_crea_total_independiente(self):
        pedido_anterior = self.crear_pedido_con_cantidad(50)
        self.pagar_pedido(pedido_anterior)

        pedido_nuevo = self.crear_pedido_con_cantidad(10)

        self.assertNotEqual(pedido_anterior.id, pedido_nuevo.id)
        self.assertEqual(pedido_anterior.total, Decimal("100.00"))
        self.assertEqual(pedido_nuevo.total, Decimal("20.00"))
        self.assertEqual(pedido_anterior.detalles.count(), 1)
        self.assertEqual(pedido_nuevo.detalles.count(), 1)

    def test_formulario_de_detalle_excluye_pedidos_pagados(self):
        pedido_pagado = self.crear_pedido_con_cantidad(5)
        self.pagar_pedido(pedido_pagado)
        pedido_abierto = Pedido.objects.create(
            vendedor=self.vendedor,
            tienda=self.tienda,
        )

        formulario = self.vendedor.configurar_formulario_detalle(
            DetallePedidoVendedorForm()
        )
        ids_disponibles = list(
            formulario.fields["pedido"].queryset.values_list("id", flat=True)
        )

        self.assertNotIn(pedido_pagado.id, ids_disponibles)
        self.assertIn(pedido_abierto.id, ids_disponibles)

    def test_vista_muestra_productos_y_cantidades_del_pedido(self):
        pedido = self.crear_pedido_con_cantidad(12)
        session = self.client.session
        session["usuario_id"] = self.vendedor.usuario_id
        session["usuario_nombre"] = self.vendedor.usuario.nombre
        session["tipo_usuario"] = "VENDEDOR"
        session.save()

        respuesta = self.client.get(reverse("detalle_pedido", args=[pedido.id]))

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Producto de prueba")
        self.assertContains(respuesta, "Proveedor Uno")
        self.assertContains(respuesta, "24.00")
        self.assertEqual(respuesta.context["detalles"].count(), 1)



class FlujoEmpresaTenderoTests(TestCase):
    def setUp(self):
        usuario_empresa = Usuario.objects.create(
            nombre="Empresa proveedora",
            correo="proveedor@empresa.com",
            contrasena="1234",
            telefono="0991000001",
            tipo_usuario="EMPRESA",
        )
        self.empresa = Empresa.objects.create(
            usuario=usuario_empresa,
            razon_social="Distribuidora Loja",
            ruc="1199999999001",
            direccion="Av. Universitaria",
            sector="Centro",
            estado_validacion="APROBADA",
        )

        usuario_tendero = Usuario.objects.create(
            nombre="Tendero principal",
            correo="compras@tienda.com",
            contrasena="1234",
            telefono="0991000002",
            tipo_usuario="TENDERO",
        )
        self.tienda = Tienda.objects.create(
            usuario=usuario_tendero,
            nombre_tienda="Tienda Central",
            ruc="1199999999002",
            direccion="Calle Bolívar",
            sector="Centro",
            estado_validacion="APROBADA",
        )

        self.producto = Producto.objects.create(
            empresa=self.empresa,
            nombre="Arroz",
            descripcion="Saco de arroz",
            precio=Decimal("10.00"),
            categoria="Alimentos",
            disponible=True,
        )
        self.inventario = Inventario.objects.create(
            producto=self.producto,
            stock_actual=100,
            stock_reservado=0,
        )

    def crear_orden_con_detalle(self, cantidad):
        pedido = PedidoEmpresa.objects.create(
            tienda=self.tienda,
            empresa=self.empresa,
        )
        detalle = DetallePedidoEmpresa(
            pedido=pedido,
            producto=self.producto,
            cantidad=cantidad,
        )
        detalle.registrar_detalle_con_reserva()
        pedido.refresh_from_db()
        self.inventario.refresh_from_db()
        return pedido

    def pagar_orden(self, pedido):
        formulario = PagoPedidoEmpresaTenderoForm(
            data={
                "pedido": pedido.id,
                "metodo_pago": "TRANSFERENCIA",
                "monto": str(pedido.total),
            }
        )
        formulario = self.tienda.configurar_formulario_pago_empresa(formulario)
        self.assertTrue(formulario.is_valid(), formulario.errors)
        self.tienda.registrar_pago_empresa(formulario)
        pedido.refresh_from_db()
        self.inventario.refresh_from_db()

    def test_agregar_producto_reserva_stock_de_empresa(self):
        pedido = self.crear_orden_con_detalle(20)

        self.assertEqual(pedido.total, Decimal("200.00"))
        self.assertEqual(self.inventario.stock_actual, 100)
        self.assertEqual(self.inventario.stock_reservado, 20)
        self.assertEqual(self.inventario.obtener_stock_disponible(), 80)

    def test_cancelar_orden_pendiente_libera_stock_reservado(self):
        pedido = self.crear_orden_con_detalle(20)
        pedido.cancelar_pedido()

        pedido.refresh_from_db()
        self.inventario.refresh_from_db()
        self.assertEqual(pedido.estado, "CANCELADO")
        self.assertEqual(self.inventario.stock_actual, 100)
        self.assertEqual(self.inventario.stock_reservado, 0)

    def test_pago_cierra_orden_y_descuenta_stock_empresa(self):
        pedido = self.crear_orden_con_detalle(20)
        self.pagar_orden(pedido)

        self.assertEqual(pedido.estado, "PAGADO")
        self.assertEqual(self.inventario.stock_actual, 80)
        self.assertEqual(self.inventario.stock_reservado, 0)
        self.assertEqual(pedido.pago.estado_pago, "APROBADO")

    def test_no_permite_agregar_producto_a_orden_pagada(self):
        pedido = self.crear_orden_con_detalle(20)
        self.pagar_orden(pedido)

        nuevo_detalle = DetallePedidoEmpresa(
            pedido=pedido,
            producto=self.producto,
            cantidad=5,
        )
        with self.assertRaisesMessage(ValueError, "orden ya está cerrada"):
            nuevo_detalle.registrar_detalle_con_reserva()

        self.assertEqual(pedido.detalles.count(), 1)

    def test_cancelar_orden_pagada_devuelve_stock_y_reembolsa(self):
        pedido = self.crear_orden_con_detalle(20)
        self.pagar_orden(pedido)
        pedido.cancelar_pedido()

        pedido.refresh_from_db()
        self.inventario.refresh_from_db()
        pago = PagoPedidoEmpresa.objects.get(pedido=pedido)

        self.assertEqual(pedido.estado, "CANCELADO")
        self.assertEqual(self.inventario.stock_actual, 100)
        self.assertEqual(self.inventario.stock_reservado, 0)
        self.assertEqual(pago.estado_pago, "REEMBOLSADO")

    def test_cancelar_en_preparacion_restaura_stock(self):
        pedido = self.crear_orden_con_detalle(20)
        self.pagar_orden(pedido)
        pedido.pasar_a_preparacion()
        pedido.cancelar_pedido()

        pedido.refresh_from_db()
        self.inventario.refresh_from_db()
        pago = PagoPedidoEmpresa.objects.get(pedido=pedido)

        self.assertEqual(pedido.estado, "CANCELADO")
        self.assertEqual(self.inventario.stock_actual, 100)
        self.assertEqual(self.inventario.stock_reservado, 0)
        self.assertEqual(pago.estado_pago, "REEMBOLSADO")

    def test_entrega_agrega_stock_a_la_tienda(self):
        pedido = self.crear_orden_con_detalle(20)
        self.pagar_orden(pedido)
        pedido.pasar_a_preparacion()
        pedido.entregar_pedido()

        pedido.refresh_from_db()
        producto_tienda = ProductoTienda.objects.get(
            tienda=self.tienda,
            producto=self.producto,
        )

        self.assertEqual(pedido.estado, "ENTREGADO")
        self.assertEqual(producto_tienda.stock_actual, 20)
        self.assertEqual(producto_tienda.stock_reservado, 0)

    def test_nueva_compra_del_mismo_producto_es_independiente(self):
        pedido_anterior = self.crear_orden_con_detalle(20)
        self.pagar_orden(pedido_anterior)

        pedido_nuevo = self.crear_orden_con_detalle(5)

        self.assertNotEqual(pedido_anterior.id, pedido_nuevo.id)
        self.assertEqual(pedido_anterior.total, Decimal("200.00"))
        self.assertEqual(pedido_nuevo.total, Decimal("50.00"))
        self.assertEqual(pedido_anterior.detalles.count(), 1)
        self.assertEqual(pedido_nuevo.detalles.count(), 1)

    def test_formulario_excluye_ordenes_pagadas(self):
        pedido_pagado = self.crear_orden_con_detalle(10)
        self.pagar_orden(pedido_pagado)
        pedido_abierto = PedidoEmpresa.objects.create(
            tienda=self.tienda,
            empresa=self.empresa,
        )

        formulario = self.tienda.configurar_formulario_detalle_empresa(
            DetallePedidoEmpresaTenderoForm()
        )
        ids_disponibles = list(
            formulario.fields["pedido"].queryset.values_list("id", flat=True)
        )

        self.assertNotIn(pedido_pagado.id, ids_disponibles)
        self.assertIn(pedido_abierto.id, ids_disponibles)

    def test_detalle_de_compra_muestra_productos_y_cantidades(self):
        pedido = self.crear_orden_con_detalle(7)
        session = self.client.session
        session["usuario_id"] = self.tienda.usuario_id
        session["usuario_nombre"] = self.tienda.usuario.nombre
        session["tipo_usuario"] = "TENDERO"
        session.save()

        respuesta = self.client.get(
            reverse("detalle_pedido_empresa_tendero", args=[pedido.id])
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Arroz")
        self.assertContains(respuesta, "Distribuidora Loja")
        self.assertContains(respuesta, "70.00")
