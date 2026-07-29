# Consolidates the shop model and the company -> shop ordering flow.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0002_alter_calificacion_puntuacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='fecha_fundacion',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='historia',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(
                choices=[
                    ('EMPRESA', 'Empresa'),
                    ('TENDERO', 'Tendero'),
                    ('VENDEDOR', 'Vendedor / Delivery'),
                ],
                max_length=30,
            ),
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tienda', models.CharField(max_length=150)),
                ('ruc', models.CharField(max_length=13, unique=True)),
                ('direccion', models.CharField(max_length=200)),
                ('sector', models.CharField(max_length=100)),
                ('fecha_apertura', models.DateField(blank=True, null=True)),
                ('descripcion_tienda', models.TextField(blank=True, default='')),
                ('referencia_ubicacion', models.CharField(blank=True, default='', max_length=200)),
                ('estado_validacion', models.CharField(
                    choices=[
                        ('PENDIENTE', 'Pendiente'),
                        ('APROBADA', 'Aprobada'),
                        ('RECHAZADA', 'Rechazada'),
                    ],
                    default='PENDIENTE',
                    max_length=30,
                )),
                ('usuario', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tienda',
                    to='comercial.usuario',
                )),
            ],
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='empresa',
        ),
        migrations.AddField(
            model_name='pedido',
            name='tienda',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='pedidos_recibidos',
                to='comercial.tienda',
            ),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='producto',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='detalles_pedido',
                to='comercial.producto',
            ),
        ),
        migrations.CreateModel(
            name='ProductoTienda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_venta', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('stock_actual', models.IntegerField(default=0)),
                ('stock_reservado', models.IntegerField(default=0)),
                ('disponible', models.BooleanField(default=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('producto', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='productos_tienda',
                    to='comercial.producto',
                )),
                ('tienda', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='productos_tienda',
                    to='comercial.tienda',
                )),
            ],
            options={
                'unique_together': {('tienda', 'producto')},
            },
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='producto_tienda',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='detalles_pedido_tienda',
                to='comercial.productotienda',
            ),
        ),
        migrations.CreateModel(
            name='PedidoEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(
                    choices=[
                        ('PENDIENTE', 'Pendiente'),
                        ('CONFIRMADO', 'Confirmado'),
                        ('PAGADO', 'Pagado'),
                        ('EN_PREPARACION', 'En preparación'),
                        ('ENTREGADO', 'Entregado'),
                        ('CANCELADO', 'Cancelado'),
                    ],
                    default='PENDIENTE',
                    max_length=30,
                )),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('empresa', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='pedidos_de_tiendas',
                    to='comercial.empresa',
                )),
                ('tienda', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='pedidos_a_empresas',
                    to='comercial.tienda',
                )),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedidoEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('precio_unitario', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pedido', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='detalles',
                    to='comercial.pedidoempresa',
                )),
                ('producto', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='detalles_pedidos_empresa',
                    to='comercial.producto',
                )),
            ],
        ),
        migrations.CreateModel(
            name='PagoPedidoEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metodo_pago', models.CharField(
                    choices=[
                        ('TARJETA', 'Tarjeta'),
                        ('TRANSFERENCIA', 'Transferencia'),
                        ('EFECTIVO', 'Efectivo'),
                        ('PASARELA', 'Pasarela de pago'),
                    ],
                    max_length=50,
                )),
                ('monto', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('estado_pago', models.CharField(
                    choices=[
                        ('PENDIENTE', 'Pendiente'),
                        ('APROBADO', 'Aprobado'),
                        ('RECHAZADO', 'Rechazado'),
                        ('REEMBOLSADO', 'Reembolsado'),
                    ],
                    default='PENDIENTE',
                    max_length=30,
                )),
                ('fecha_pago', models.DateTimeField(auto_now_add=True)),
                ('pedido', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='pago',
                    to='comercial.pedidoempresa',
                )),
            ],
        ),
    ]
