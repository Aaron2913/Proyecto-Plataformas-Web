# Corrección del manejo de stock

Se corrigió el proyecto para que las funciones de negocio estén en `models.py` y las vistas solo las llamen.

## Flujo corregido

```text
Empresa proveedora -> Tienda / Tendero -> Vendedor / Delivery
```

## Reglas implementadas

1. Cuando el tendero agrega un producto a su tienda, el stock se descuenta del inventario de la empresa proveedora.
2. Cuando el delivery agrega un producto a un pedido, el stock de la tienda se reserva.
3. Cuando el pedido se cancela, el stock reservado se libera.
4. Cuando el pago está aprobado, el stock reservado se descuenta definitivamente del stock de la tienda.
5. El tendero puede confirmar, preparar y entregar pedidos.

## Métodos principales agregados o usados en models.py

- `Tienda.crear_producto_tienda(formulario)`
- `Tienda.confirmar_pedido(pedido_id)`
- `Tienda.pasar_pedido_a_preparacion(pedido_id)`
- `Tienda.entregar_pedido(pedido_id)`
- `Vendedor.agregar_detalle_pedido(formulario)`
- `Vendedor.registrar_pago(formulario)`
- `Vendedor.cancelar_pedido(pedido_id)`
- `DetallePedido.registrar_detalle_con_reserva()`
- `Pedido.pagar_y_descontar_stock()`
- `Pedido.cancelar_pedido()`
- `ProductoTienda.reservar_stock(cantidad)`
- `ProductoTienda.liberar_stock(cantidad)`
- `ProductoTienda.descontar_stock(cantidad)`

## Vistas corregidas

Las vistas ya no hacen directamente el manejo de stock con `formulario.save()`. Ahora llaman métodos del modelo:

- `crear_producto_tendero()` llama `tienda.crear_producto_tienda(formulario)`
- `crear_detalle_vendedor()` llama `vendedor.agregar_detalle_pedido(formulario)`
- `crear_pago_vendedor()` llama `vendedor.registrar_pago(formulario)`
- `cancelar_pedido_vendedor()` llama `vendedor.cancelar_pedido(pedido_id)`
- `confirmar_pedido_tendero()` llama `tienda.confirmar_pedido(pedido_id)`
- `preparar_pedido_tendero()` llama `tienda.pasar_pedido_a_preparacion(pedido_id)`
- `entregar_pedido_tendero()` llama `tienda.entregar_pedido(pedido_id)`

## Nota

No se agregaron campos nuevos a la base de datos en esta corrección. Por eso, normalmente no se requiere crear una nueva migración. Igual se puede ejecutar:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
