# Cambios realizados: nuevo rol TENDERO

## Flujo actualizado

Empresa proveedora -> Tienda/Tendero -> Vendedor/Delivery

La empresa ya no vende directamente al delivery. La empresa registra productos, el tendero selecciona productos de una empresa proveedora para su tienda y el delivery crea pedidos directamente a una tienda.

## Archivos modificados

- comercial/models.py
- comercial/forms.py
- comercial/views.py
- comercial/urls.py
- comercial/admin.py
- comercial/serializers.py
- comercial/templates/comercial/base.html
- comercial/templates/comercial/login.html
- comercial/templates/comercial/registro_empresa.html
- comercial/templates/comercial/registro_tendero.html
- comercial/templates/comercial/registro_vendedor.html
- comercial/templates/comercial/inicio_empresa.html
- comercial/templates/comercial/inicio_tendero.html
- comercial/templates/comercial/inicio_vendedor.html
- comercial/templates/comercial/tiendas_empresa.html
- comercial/templates/comercial/productos_tendero.html
- comercial/templates/comercial/pedidos_tendero.html
- comercial/templates/comercial/catalogo_vendedor.html
- comercial/templates/comercial/pedidos_vendedor.html
- comercial/templates/comercial/pagos_vendedor.html

## Nuevos modelos

- Tienda
- ProductoTienda

## Cambios importantes en modelos existentes

- Usuario ahora acepta tres roles: EMPRESA, TENDERO y VENDEDOR.
- Pedido ahora se realiza hacia una tienda.
- Pedido mantiene empresa como empresa proveedora, pero se llena automáticamente desde la tienda.
- DetallePedido ahora puede trabajar con ProductoTienda para descontar stock de tienda.

## Vistas simplificadas

Las reglas de negocio quedaron en models.py. Views.py ahora se encarga principalmente de:

- Validar sesión.
- Validar rol.
- Crear formularios.
- Llamar métodos del modelo.
- Renderizar templates.

## Comandos para aplicar cambios

Después de copiar estos archivos en el proyecto, ejecutar:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Orden de prueba recomendado

1. Registrar una empresa.
2. Iniciar sesión como empresa y registrar productos.
3. Registrar un tendero seleccionando una empresa proveedora.
4. Iniciar sesión como tendero y agregar productos a la tienda.
5. Registrar un delivery.
6. Iniciar sesión como delivery, revisar catálogo de tiendas, crear pedido, agregar productos y registrar pago.
