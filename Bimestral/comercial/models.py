from django.db import models

# Create your models here.


class Usuario(models.Model):
    TIPO_USUARIO = (
        ("EMPRESA", "Empresa"),
        ("VENDEDOR", "Vendedor"),
    )

    ESTADO_USUARIO = (
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    )

    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=30, choices=ESTADO_USUARIO, default="ACTIVO")
    tipo_usuario = models.CharField(max_length=30, choices=TIPO_USUARIO)

    def __str__(self):
        return "%s %s" % (self.nombre, self.correo)

    def obtener_notificaciones(self):
        return self.notificaciones.count()

    def esta_activo(self):
        if self.estado == "ACTIVO":
            return "Usuario activo"
        else:
            return "Usuario inactivo"


class Empresa(models.Model):
    ESTADO_VALIDACION = (
        ("PENDIENTE", "Pendiente"),
        ("APROBADA", "Aprobada"),
        ("RECHAZADA", "Rechazada"),
    )

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="empresa"
    )
    razon_social = models.CharField(max_length=150)
    ruc = models.CharField(max_length=13, unique=True)
    direccion = models.CharField(max_length=200)
    sector = models.CharField(max_length=100)
    limite_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_base_sector = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado_validacion = models.CharField(
        max_length=30,
        choices=ESTADO_VALIDACION,
        default="PENDIENTE"
    )

    def __str__(self):
        return "%s %s" % (self.razon_social, self.ruc)

    def obtener_productos(self):
        return self.productos.count()

    def obtener_pedidos_recibidos(self):
        return self.pedidos_recibidos.count()

    def obtener_calificaciones(self):
        return self.calificaciones.count()

    def esta_aprobada(self):
        if self.estado_validacion == "APROBADA":
            return "Empresa aprobada"
        else:
            return "Empresa no aprobada"

    def validar_empresa(self):
        self.estado_validacion = "APROBADA"
        self.save()
        return "Empresa validada correctamente"


class Vendedor(models.Model):
    ESTADO_VALIDACION = (
        ("PENDIENTE", "Pendiente"),
        ("APROBADO", "Aprobado"),
        ("RECHAZADO", "Rechazado"),
    )

    NIVEL_VENDEDOR = (
        ("NUEVO", "Nuevo"),
        ("BRONCE", "Bronce"),
        ("PLATA", "Plata"),
        ("ORO", "Oro"),
        ("ESTRELLA", "Vendedor estrella"),
    )

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="vendedor"
    )
    cedula = models.CharField(max_length=10, unique=True)
    direccion = models.CharField(max_length=200)
    calificacion = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_ventas = models.IntegerField(default=0)
    nivel = models.CharField(max_length=30, choices=NIVEL_VENDEDOR, default="NUEVO")
    estado_validacion = models.CharField(
        max_length=30,
        choices=ESTADO_VALIDACION,
        default="PENDIENTE"
    )

    def __str__(self):
        return "%s %s" % (self.usuario.nombre, self.cedula)

    def obtener_pedidos(self):
        return self.pedidos.count()

    def obtener_calificaciones_realizadas(self):
        return self.calificaciones_realizadas.count()

    def obtener_tutoriales_consultados(self):
        return self.tutoriales_consultados.count()

    def es_vendedor_aprobado(self):
        if self.estado_validacion == "APROBADO":
            return "Vendedor aprobado"
        else:
            return "Vendedor no aprobado"

    def obtener_nivel_vendedor(self):
        if self.total_ventas >= 100:
            return "ESTRELLA"
        elif self.total_ventas >= 50:
            return "ORO"
        elif self.total_ventas >= 20:
            return "PLATA"
        elif self.total_ventas >= 5:
            return "BRONCE"
        else:
            return "NUEVO"

    def actualizar_nivel(self):
        self.nivel = self.obtener_nivel_vendedor()
        self.save()
        return self.nivel


class Producto(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="productos"
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return "%s %s" % (self.nombre, self.empresa.razon_social)

    def obtener_stock_disponible(self):
        if hasattr(self, "inventario"):
            return self.inventario.stock_actual - self.inventario.stock_reservado
        else:
            return 0

    def esta_disponible(self):
        if self.disponible and self.obtener_stock_disponible() > 0:
            return "Disponible"
        else:
            return "No disponible"

    def cambiar_disponibilidad(self):
        if self.disponible:
            self.disponible = False
        else:
            self.disponible = True

        self.save()
        return self.esta_disponible()


class Inventario(models.Model):
    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,
        related_name="inventario"
    )
    stock_actual = models.IntegerField(default=0)
    stock_reservado = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s Stock actual: %s" % (self.producto.nombre, self.stock_actual)

    def obtener_stock_disponible(self):
        return self.stock_actual - self.stock_reservado

    def verificar_stock(self):
        if self.obtener_stock_disponible() > 0:
            return "Con stock"
        else:
            return "Sin stock"

    def reservar_stock(self, cantidad):
        if cantidad <= self.obtener_stock_disponible():
            self.stock_reservado = self.stock_reservado + cantidad
            self.save()
            return "Stock reservado"
        else:
            return "Stock insuficiente"

    def liberar_stock(self, cantidad):
        if cantidad <= self.stock_reservado:
            self.stock_reservado = self.stock_reservado - cantidad
            self.save()
            return "Stock liberado"
        else:
            return "Cantidad incorrecta"

    def descontar_stock(self, cantidad):
        if cantidad <= self.stock_actual:
            self.stock_actual = self.stock_actual - cantidad

            if cantidad <= self.stock_reservado:
                self.stock_reservado = self.stock_reservado - cantidad

            self.save()
            return "Stock descontado"
        else:
            return "Stock insuficiente"


class Pedido(models.Model):
    ESTADO_PEDIDO = (
        ("PENDIENTE", "Pendiente"),
        ("CONFIRMADO", "Confirmado"),
        ("PAGADO", "Pagado"),
        ("EN_PREPARACION", "En preparación"),
        ("ENTREGADO", "Entregado"),
        ("CANCELADO", "Cancelado"),
    )

    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="pedidos_recibidos"
    )
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, choices=ESTADO_PEDIDO, default="PENDIENTE")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "Pedido %s %s" % (self.id, self.estado)

    def obtener_detalles(self):
        return self.detalles.count()

    def obtener_total(self):
        total = 0
        detalles = self.detalles.all()

        for detalle in detalles:
            total = total + detalle.subtotal

        return total

    def actualizar_total(self):
        total = self.obtener_total()
        self.subtotal = total
        self.total = total
        self.save()
        return self.total

    def consultar_estado(self):
        return self.estado

    def reservar_productos(self):
        detalles = self.detalles.all()

        for detalle in detalles:
            if hasattr(detalle.producto, "inventario"):
                detalle.producto.inventario.reservar_stock(detalle.cantidad)

        return "Productos reservados"

    def confirmar_pedido(self):
        detalles = self.detalles.all()

        for detalle in detalles:
            if hasattr(detalle.producto, "inventario"):
                detalle.producto.inventario.descontar_stock(detalle.cantidad)

        self.estado = "CONFIRMADO"
        self.save()
        return "Pedido confirmado"

    def pasar_a_preparacion(self):
        if self.estado == "PAGADO":
            self.estado = "EN_PREPARACION"
            self.save()
            return "Pedido en preparación"
        else:
            return "El pedido debe estar pagado"

    def entregar_pedido(self):
        if self.estado == "EN_PREPARACION":
            self.estado = "ENTREGADO"
            self.save()

            self.vendedor.total_ventas = self.vendedor.total_ventas + 1
            self.vendedor.actualizar_nivel()

            return "Pedido entregado"
        else:
            return "El pedido debe estar en preparación"

    def cancelar_pedido(self):
        if self.estado == "PENDIENTE":
            detalles = self.detalles.all()

            for detalle in detalles:
                if hasattr(detalle.producto, "inventario"):
                    detalle.producto.inventario.liberar_stock(detalle.cantidad)

            self.estado = "CANCELADO"
            self.save()
            return "Pedido cancelado"
        else:
            return "El pedido no se puede cancelar"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="detalles_pedido"
    )
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "%s %s" % (self.producto.nombre, self.cantidad)

    def calcular_subtotal(self):
        return self.cantidad * self.precio_unitario

    def actualizar_subtotal(self):
        self.subtotal = self.calcular_subtotal()
        self.save()
        self.pedido.actualizar_total()
        return self.subtotal

    def save(self, *args, **kwargs):
        if self.precio_unitario == 0:
            self.precio_unitario = self.producto.precio

        self.subtotal = self.calcular_subtotal()
        super().save(*args, **kwargs)

        self.pedido.actualizar_total()


class Pago(models.Model):
    METODO_PAGO = (
        ("TARJETA", "Tarjeta"),
        ("TRANSFERENCIA", "Transferencia"),
        ("EFECTIVO", "Efectivo"),
        ("PASARELA", "Pasarela de pago"),
    )

    ESTADO_PAGO = (
        ("PENDIENTE", "Pendiente"),
        ("APROBADO", "Aprobado"),
        ("RECHAZADO", "Rechazado"),
        ("REEMBOLSADO", "Reembolsado"),
    )

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name="pago"
    )
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado_pago = models.CharField(max_length=30, choices=ESTADO_PAGO, default="PENDIENTE")
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Pago pedido %s %s" % (self.pedido.id, self.estado_pago)

    def pago_aprobado(self):
        if self.estado_pago == "APROBADO":
            return "Pago aprobado"
        else:
            return "Pago pendiente o rechazado"

    def validar_pago(self):
        if self.estado_pago == "APROBADO":
            self.pedido.estado = "PAGADO"
            self.pedido.save()
            return "Pago validado y pedido actualizado"
        else:
            return "El pago no está aprobado"

    def registrar_reembolso(self):
        self.estado_pago = "REEMBOLSADO"
        self.save()
        return "Reembolso registrado"


class Factura(models.Model):
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name="factura"
    )
    numero_factura = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "%s %s" % (self.numero_factura, self.total)

    def obtener_cliente(self):
        return self.pedido.vendedor.usuario.nombre

    def obtener_empresa(self):
        return self.pedido.empresa.razon_social

    def obtener_total_factura(self):
        return self.total

    def actualizar_total_factura(self):
        self.total = self.pedido.total
        self.save()
        return self.total

    def save(self, *args, **kwargs):
        self.total = self.pedido.total
        super().save(*args, **kwargs)


class Comision(models.Model):
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name="comision"
    )
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valor_comision = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_calculo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Comisión pedido %s %s" % (self.pedido.id, self.valor_comision)

    def calcular_comision(self):
        return (self.pedido.total * self.porcentaje) / 100

    def actualizar_comision(self):
        self.valor_comision = self.calcular_comision()
        self.save()
        return self.valor_comision

    def save(self, *args, **kwargs):
        self.valor_comision = self.calcular_comision()
        super().save(*args, **kwargs)


class Suscripcion(models.Model):
    TIPO_SUSCRIPCION = (
        ("ANUAL", "Pago anual"),
        ("COMISION", "Por comisión"),
    )

    ESTADO_SUSCRIPCION = (
        ("ACTIVA", "Activa"),
        ("VENCIDA", "Vencida"),
        ("CANCELADA", "Cancelada"),
    )

    empresa = models.OneToOneField(
        Empresa,
        on_delete=models.CASCADE,
        related_name="suscripcion"
    )
    tipo = models.CharField(max_length=50, choices=TIPO_SUSCRIPCION, default="ANUAL")
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=30, choices=ESTADO_SUSCRIPCION, default="ACTIVA")

    def __str__(self):
        return "%s %s" % (self.empresa.razon_social, self.tipo)

    def obtener_estado(self):
        return self.estado

    def esta_activa(self):
        if self.estado == "ACTIVA":
            return "Suscripción activa"
        else:
            return "Suscripción no activa"

    def cancelar_suscripcion(self):
        self.estado = "CANCELADA"
        self.save()
        return "Suscripción cancelada"


class Calificacion(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="calificaciones"
    )
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE,
        related_name="calificaciones_realizadas"
    )
    puntuacion = models.IntegerField(default=1)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.empresa.razon_social, self.puntuacion)

    def obtener_comentario(self):
        return self.comentario

    def es_buena_calificacion(self):
        if self.puntuacion >= 4:
            return "Buena calificación"
        else:
            return "Calificación baja"


class Notificacion(models.Model):
    TIPO_NOTIFICACION = (
        ("PEDIDO", "Pedido"),
        ("PAGO", "Pago"),
        ("STOCK", "Stock"),
        ("SISTEMA", "Sistema"),
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="notificaciones"
    )
    tipo = models.CharField(max_length=50, choices=TIPO_NOTIFICACION)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.usuario.nombre, self.tipo)

    def estado_lectura(self):
        if self.leida:
            return "Leída"
        else:
            return "No leída"

    def marcar_como_leida(self):
        self.leida = True
        self.save()
        return "Notificación marcada como leída"


class Tutorial(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    url_contenido = models.URLField()
    vendedores = models.ManyToManyField(
        Vendedor,
        related_name="tutoriales_consultados",
        blank=True
    )

    def __str__(self):
        return "%s" % (self.titulo)

    def obtener_vendedores(self):
        return self.vendedores.count()