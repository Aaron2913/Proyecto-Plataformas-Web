# Corrección del flujo de tendero multiempresa

## Problema corregido

Antes, al registrar un tendero se le obligaba a seleccionar una sola empresa proveedora. Esa lógica estaba mal porque una tienda puede vender productos de varias empresas.

## Flujo corregido

Empresa proveedora -> Producto con inventario -> Tienda selecciona productos -> Delivery compra en tienda

## Regla principal

El tendero ya no se asocia directamente a una empresa en el registro. El tendero registra su tienda y, al agregar productos, puede escoger productos disponibles de cualquier empresa proveedora que tenga stock.

## Manejo del stock

1. La empresa registra productos e inventario.
2. El tendero agrega productos disponibles a su tienda.
3. Al agregar productos, se descuenta stock del inventario de la empresa dueña de ese producto.
4. El delivery crea un pedido a una tienda.
5. Al agregar productos al pedido, se reserva stock de la tienda.
6. Si cancela el pedido, se libera el stock reservado.
7. Si paga, se descuenta definitivamente el stock de la tienda.

## Archivos modificados

- comercial/models.py
- comercial/forms.py
- comercial/serializers.py
- comercial/templates/comercial/inicio_tendero.html
- comercial/templates/comercial/tiendas_empresa.html
- comercial/templates/comercial/pedidos_empresa.html
- comercial/templates/comercial/productos_tendero.html
