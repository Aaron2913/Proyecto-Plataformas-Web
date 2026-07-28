from django.db import models, transaction


class Usuario(models.Model):
    TIPO_USUARIO = (
        ("EMPRESA", "Empresa"),
        ("TENDERO", "Tendero"),
        ("VENDEDOR", "Vendedor / Delivery"),
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

    @classmethod
    def autenticar(cls, correo, contrasena):
        return cls.objects.filter(
            correo=correo,
            contrasena=contrasena,
            estado="ACTIVO"
        ).first()

    @classmethod
    def obtener_por_id(cls, usuario_id):
        return cls.objects.get(id=usuario_id)

    def guardar_en_sesion(self, request):
        request.session["usuario_id"] = self.id
        request.session["usuario_nombre"] = self.nombre
        request.session["tipo_usuario"] = self.tipo_usuario
        return "Sesión iniciada"

    def obtener_notificaciones(self):
        return self.notificaciones.count()

    def esta_activo(self):
        if self.estado == "ACTIVO":
            return "Usuario activo"
        else:
            return "Usuario inactivo"

    def obtener_inicio_por_rol(self):
        if self.tipo_usuario == "EMPRESA":
            return "inicio_empresa"

        if self.tipo_usuario == "TENDERO":
            return "inicio_tendero"

        if self.tipo_usuario == "VENDEDOR":
            return "inicio_vendedor"

        return "login"


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

    @classmethod
    def obtener_por_usuario_id(cls, usuario_id):
        usuario = Usuario.obtener_por_id(usuario_id)
        return cls.objects.get(usuario=usuario)

    @classmethod
    def registrar_desde_formularios(cls, formulario_usuario, formulario_empresa):
        usuario = formulario_usuario.save(commit=False)
        usuario.estado = "ACTIVO"
        usuario.tipo_usuario = "EMPRESA"
        usuario.save()

        empresa = formulario_empresa.save(commit=False)
        empresa.usuario = usuario
        empresa.estado_validacion = "PENDIENTE"
        empresa.save()

        return empresa

    def listar_productos(self):
        return self.productos.all()

    def listar_inventarios(self):
        return Inventario.objects.filter(producto__empresa=self)

    def listar_tiendas(self):
        return self.tiendas.all()

    def listar_pedidos_recibidos(self):
        return Pedido.objects.filter(empresa=self)

    def contar_productos(self):
        return self.listar_productos().count()

    def contar_inventarios(self):
        return self.listar_inventarios().count()

    def contar_tiendas(self):
        return self.listar_tiendas().count()

    def contar_pedidos_recibidos(self):
        return self.listar_pedidos_recibidos().count()

    def obtener_productos(self):
        return self.contar_productos()

    def obtener_pedidos_recibidos(self):
        return self.contar_pedidos_recibidos()

    def obtener_calificaciones(self):
        return self.calificaciones.count()

    def obtener_resumen_dashboard(self):
        return {
            "empresa": self,
            "total_productos": self.contar_productos(),
            "total_inventarios": self.contar_inventarios(),
            "total_tiendas": self.contar_tiendas(),
            "total_pedidos": self.contar_pedidos_recibidos(),
        }

    def crear_producto(self, formulario):
        producto = formulario.save(commit=False)
        producto.empresa = self
        producto.save()
        return producto

    def configurar_formulario_inventario(self, formulario):
        formulario.fields["producto"].queryset = self.listar_productos()
        return formulario

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

    @classmethod
    def obtener_por_usuario_id(cls, usuario_id):
        usuario = Usuario.obtener_por_id(usuario_id)
        return cls.objects.get(usuario=usuario)

    @classmethod
    def registrar_desde_formularios(cls, formulario_usuario, formulario_vendedor):
        usuario = formulario_usuario.save(commit=False)
        usuario.estado = "ACTIVO"
        usuario.tipo_usuario = "VENDEDOR"
        usuario.save()

        vendedor = formulario_vendedor.save(commit=False)
        vendedor.usuario = usuario
        vendedor.calificacion = 0
        vendedor.total_ventas = 0
        vendedor.nivel = "NUEVO"
        vendedor.estado_validacion = "PENDIENTE"
        vendedor.save()

        return vendedor

    def listar_tiendas(self):
        return Tienda.objects.filter(estado_validacion="APROBADA")

    def listar_catalogo(self):
        return ProductoTienda.objects.filter(disponible=True)

    def listar_pedidos(self):
        return self.pedidos.all()

    def listar_pagos(self):
        return Pago.objects.filter(pedido__vendedor=self)

    def contar_productos_disponibles(self):
        return self.listar_catalogo().count()

    def contar_pedidos(self):
        return self.listar_pedidos().count()

    def contar_pagos(self):
        return self.listar_pagos().count()

    def obtener_resumen_dashboard(self):
        return {
            "vendedor": self,
            "total_productos": self.contar_productos_disponibles(),
            "total_pedidos": self.contar_pedidos(),
            "total_pagos": self.contar_pagos(),
        }

    def crear_pedido(self, formulario):
        pedido = formulario.save(commit=False)
        pedido.vendedor = self
        pedido.estado = "PENDIENTE"
        pedido.subtotal = 0
        pedido.total = 0

        if pedido.tienda is not None:
            pedido.empresa = pedido.tienda.empresa

        pedido.save()
        return pedido

    def configurar_formulario_detalle(self, formulario):
        formulario.fields["pedido"].queryset = self.listar_pedidos().filter(estado__in=["PENDIENTE", "CONFIRMADO"])
        formulario.fields["producto_tienda"].queryset = ProductoTienda.objects.filter(
            disponible=True,
            stock_actual__gt=models.F("stock_reservado")
        )
        return formulario

    def configurar_formulario_pago(self, formulario):
        formulario.fields["pedido"].queryset = self.listar_pedidos().filter(estado__in=["PENDIENTE", "CONFIRMADO"])
        return formulario

    def agregar_detalle_pedido(self, formulario):
        detalle = formulario.save(commit=False)

        if detalle.pedido.vendedor != self:
            raise ValueError("El pedido seleccionado no pertenece al vendedor actual.")

        return detalle.registrar_detalle_con_reserva()

    def registrar_pago(self, formulario):
        pago = formulario.save(commit=False)

        if pago.pedido.vendedor != self:
            raise ValueError("El pedido seleccionado no pertenece al vendedor actual.")

        if pago.monto <= 0:
            raise ValueError("El monto del pago debe ser mayor a cero.")

        pago.save()
        pago.validar_pago()
        return pago

    def cancelar_pedido(self, pedido_id):
        pedido = self.pedidos.get(id=pedido_id)
        return pedido.cancelar_pedido()

    def obtener_pedidos(self):
        return self.contar_pedidos()

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


class Tienda(models.Model):
    ESTADO_VALIDACION = (
        ("PENDIENTE", "Pendiente"),
        ("APROBADA", "Aprobada"),
        ("RECHAZADA", "Rechazada"),
    )

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="tienda"
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="tiendas"
    )
    nombre_tienda = models.CharField(max_length=150)
    ruc = models.CharField(max_length=13, unique=True)
    direccion = models.CharField(max_length=200)
    sector = models.CharField(max_length=100)
    estado_validacion = models.CharField(
        max_length=30,
        choices=ESTADO_VALIDACION,
        default="PENDIENTE"
    )

    def __str__(self):
        return "%s %s" % (self.nombre_tienda, self.ruc)

    @classmethod
    def obtener_por_usuario_id(cls, usuario_id):
        usuario = Usuario.obtener_por_id(usuario_id)
        return cls.objects.get(usuario=usuario)

    @classmethod
    def registrar_desde_formularios(cls, formulario_usuario, formulario_tienda):
        usuario = formulario_usuario.save(commit=False)
        usuario.estado = "ACTIVO"
        usuario.tipo_usuario = "TENDERO"
        usuario.save()

        tienda = formulario_tienda.save(commit=False)
        tienda.usuario = usuario
        tienda.estado_validacion = "PENDIENTE"
        tienda.save()

        return tienda

    def listar_productos_tienda(self):
        return self.productos_tienda.all()

    def listar_pedidos_recibidos(self):
        return self.pedidos_recibidos.all()

    def contar_productos_tienda(self):
        return self.listar_productos_tienda().count()

    def contar_pedidos_recibidos(self):
        return self.listar_pedidos_recibidos().count()

    def obtener_resumen_dashboard(self):
        return {
            "tienda": self,
            "total_productos": self.contar_productos_tienda(),
            "total_pedidos": self.contar_pedidos_recibidos(),
            "empresa_proveedora": self.empresa,
        }

    def configurar_formulario_producto_tienda(self, formulario):
        formulario.fields["producto"].queryset = Producto.objects.filter(empresa=self.empresa)
        return formulario

    def crear_producto_tienda(self, formulario):
        """
        Registra o repone un producto dentro de la tienda y transfiere stock
        desde el inventario de la empresa proveedora hacia el inventario de la tienda.

        Esta es la regla principal del flujo:
        Empresa proveedora -> Tienda -> Delivery.
        """
        with transaction.atomic():
            producto_tienda_form = formulario.save(commit=False)
            producto_tienda_form.tienda = self
            cantidad_recibida = producto_tienda_form.stock_actual

            if producto_tienda_form.producto.empresa != self.empresa:
                raise ValueError("El producto no pertenece a la empresa proveedora de esta tienda.")

            if cantidad_recibida <= 0:
                raise ValueError("La cantidad de stock debe ser mayor a cero.")

            if not hasattr(producto_tienda_form.producto, "inventario"):
                raise ValueError("El producto no tiene inventario registrado en la empresa.")

            inventario_empresa = producto_tienda_form.producto.inventario

            if not inventario_empresa.puede_descontar_stock(cantidad_recibida):
                raise ValueError("La empresa no tiene stock suficiente para entregar a la tienda.")

            inventario_empresa.descontar_stock(cantidad_recibida)

            producto_tienda_existente = ProductoTienda.objects.filter(
                tienda=self,
                producto=producto_tienda_form.producto
            ).first()

            if producto_tienda_existente is not None:
                producto_tienda_existente.stock_actual = producto_tienda_existente.stock_actual + cantidad_recibida
                producto_tienda_existente.precio_venta = producto_tienda_form.precio_venta
                producto_tienda_existente.disponible = producto_tienda_form.disponible
                producto_tienda_existente.save()
                return producto_tienda_existente

            producto_tienda_form.stock_reservado = 0
            producto_tienda_form.save()
            return producto_tienda_form

    def confirmar_pedido(self, pedido_id):
        pedido = self.pedidos_recibidos.get(id=pedido_id)
        return pedido.confirmar_pedido()

    def pasar_pedido_a_preparacion(self, pedido_id):
        pedido = self.pedidos_recibidos.get(id=pedido_id)
        return pedido.pasar_a_preparacion()

    def entregar_pedido(self, pedido_id):
        pedido = self.pedidos_recibidos.get(id=pedido_id)
        return pedido.entregar_pedido()

    def esta_aprobada(self):
        if self.estado_validacion == "APROBADA":
            return "Tienda aprobada"
        else:
            return "Tienda no aprobada"

    def validar_tienda(self):
        self.estado_validacion = "APROBADA"
        self.save()
        return "Tienda validada correctamente"


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

    def listar_tiendas(self):
        return self.productos_tienda.all()

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

    def puede_reservar_stock(self, cantidad):
        return cantidad > 0 and cantidad <= self.obtener_stock_disponible()

    def puede_descontar_stock(self, cantidad):
        return cantidad > 0 and cantidad <= self.obtener_stock_disponible()

    def reservar_stock(self, cantidad):
        if self.puede_reservar_stock(cantidad):
            self.stock_reservado = self.stock_reservado + cantidad
            self.save()
            return "Stock reservado"
        else:
            return "Stock insuficiente"

    def liberar_stock(self, cantidad):
        if cantidad > 0 and cantidad <= self.stock_reservado:
            self.stock_reservado = self.stock_reservado - cantidad
            self.save()
            return "Stock liberado"
        else:
            return "Cantidad incorrecta"

    def descontar_stock(self, cantidad):
        if self.puede_descontar_stock(cantidad) or cantidad <= self.stock_actual:
            self.stock_actual = self.stock_actual - cantidad

            if cantidad <= self.stock_reservado:
                self.stock_reservado = self.stock_reservado - cantidad

            self.save()
            return "Stock descontado"
        else:
            return "Stock insuficiente"


class ProductoTienda(models.Model):
    tienda = models.ForeignKey(
        Tienda,
        on_delete=models.CASCADE,
        related_name="productos_tienda"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="productos_tienda"
    )
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_actual = models.IntegerField(default=0)
    stock_reservado = models.IntegerField(default=0)
    disponible = models.BooleanField(default=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("tienda", "producto")

    def __str__(self):
        return "%s - %s" % (self.tienda.nombre_tienda, self.producto.nombre)

    def obtener_stock_disponible(self):
        return self.stock_actual - self.stock_reservado

    def esta_disponible(self):
        if self.disponible and self.obtener_stock_disponible() > 0:
            return "Disponible"
        else:
            return "No disponible"

    def puede_reservar_stock(self, cantidad):
        return cantidad > 0 and cantidad <= self.obtener_stock_disponible()

    def puede_descontar_stock(self, cantidad):
        return cantidad > 0 and cantidad <= self.stock_actual

    def reservar_stock(self, cantidad):
        if self.puede_reservar_stock(cantidad):
            self.stock_reservado = self.stock_reservado + cantidad
            self.save()
            return "Stock de tienda reservado"
        else:
            return "Stock insuficiente en tienda"

    def liberar_stock(self, cantidad):
        if cantidad > 0 and cantidad <= self.stock_reservado:
            self.stock_reservado = self.stock_reservado - cantidad
            self.save()
            return "Stock de tienda liberado"
        else:
            return "Cantidad incorrecta"

    def descontar_stock(self, cantidad):
        if self.puede_descontar_stock(cantidad):
            self.stock_actual = self.stock_actual - cantidad

            if cantidad <= self.stock_reservado:
                self.stock_reservado = self.stock_reservado - cantidad

            self.save()
            return "Stock de tienda descontado"
        else:
            return "Stock insuficiente en tienda"

    def save(self, *args, **kwargs):
        if self.precio_venta == 0:
            self.precio_venta = self.producto.precio

        super().save(*args, **kwargs)


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
        related_name="pedidos_recibidos",
        null=True,
        blank=True
    )
    tienda = models.ForeignKey(
        Tienda,
        on_delete=models.CASCADE,
        related_name="pedidos_recibidos",
        null=True,
        blank=True
    )
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, choices=ESTADO_PEDIDO, default="PENDIENTE")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "Pedido %s %s" % (self.id, self.estado)

    def obtener_detalles(self):
        return self.detalles.count()

    def obtener_nombre_tienda(self):
        if self.tienda is not None:
            return self.tienda.nombre_tienda
        else:
            return "Sin tienda"

    def obtener_empresa_proveedora(self):
        if self.empresa is not None:
            return self.empresa.razon_social
        elif self.tienda is not None:
            return self.tienda.empresa.razon_social
        else:
            return "Sin empresa"

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
            resultado = detalle.reservar_stock()

            if "insuficiente" in resultado.lower() or "no existe" in resultado.lower():
                raise ValueError(resultado)

        return "Productos reservados"

    def confirmar_pedido(self):
        if self.estado != "PENDIENTE":
            return "El pedido no está pendiente"

        if self.detalles.count() == 0:
            return "El pedido no tiene productos"

        self.estado = "CONFIRMADO"
        self.save()
        return "Pedido confirmado"

    def pagar_y_descontar_stock(self):
        if self.estado not in ["PENDIENTE", "CONFIRMADO"]:
            raise ValueError("El pedido no se puede pagar en este estado")

        if self.detalles.count() == 0:
            raise ValueError("El pedido no tiene productos")

        with transaction.atomic():
            for detalle in self.detalles.all():
                resultado = detalle.descontar_stock()

                if "insuficiente" in resultado.lower() or "no existe" in resultado.lower():
                    raise ValueError(resultado)

            self.estado = "PAGADO"
            self.save()

        return "Pedido pagado y stock descontado"

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
        if self.estado in ["PENDIENTE", "CONFIRMADO"]:
            with transaction.atomic():
                detalles = self.detalles.all()

                for detalle in detalles:
                    detalle.liberar_stock()

                self.estado = "CANCELADO"
                self.save()

            return "Pedido cancelado y stock reservado liberado"
        else:
            return "El pedido no se puede cancelar"

    def save(self, *args, **kwargs):
        if self.tienda is not None:
            self.empresa = self.tienda.empresa

        super().save(*args, **kwargs)


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="detalles_pedido",
        null=True,
        blank=True
    )
    producto_tienda = models.ForeignKey(
        ProductoTienda,
        on_delete=models.CASCADE,
        related_name="detalles_pedido_tienda",
        null=True,
        blank=True
    )
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "%s %s" % (self.obtener_nombre_producto(), self.cantidad)

    def obtener_nombre_producto(self):
        if self.producto_tienda is not None:
            return self.producto_tienda.producto.nombre

        if self.producto is not None:
            return self.producto.nombre

        return "Sin producto"

    def obtener_tienda(self):
        if self.producto_tienda is not None:
            return self.producto_tienda.tienda

        return None

    def calcular_subtotal(self):
        return self.cantidad * self.precio_unitario

    def actualizar_subtotal(self):
        self.subtotal = self.calcular_subtotal()
        self.save()
        self.pedido.actualizar_total()
        return self.subtotal

    def validar_detalle_tienda(self):
        if self.producto_tienda is None:
            raise ValueError("Debe seleccionar un producto de una tienda.")

        if self.pedido.tienda != self.producto_tienda.tienda:
            raise ValueError("El producto seleccionado no pertenece a la tienda del pedido.")

        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        if not self.producto_tienda.puede_reservar_stock(self.cantidad):
            raise ValueError("Stock insuficiente en la tienda.")

        return True

    def registrar_detalle_con_reserva(self):
        with transaction.atomic():
            self.validar_detalle_tienda()

            if self.producto_tienda is not None:
                self.producto = self.producto_tienda.producto

                if self.precio_unitario == 0:
                    self.precio_unitario = self.producto_tienda.precio_venta

            self.subtotal = self.calcular_subtotal()
            resultado = self.reservar_stock()

            if "insuficiente" in resultado.lower() or "no existe" in resultado.lower():
                raise ValueError(resultado)

            self.save()
            self.pedido.actualizar_total()

            return self

    def reservar_stock(self):
        if self.producto_tienda is not None:
            return self.producto_tienda.reservar_stock(self.cantidad)

        if self.producto is not None and hasattr(self.producto, "inventario"):
            return self.producto.inventario.reservar_stock(self.cantidad)

        return "No existe inventario"

    def liberar_stock(self):
        if self.producto_tienda is not None:
            return self.producto_tienda.liberar_stock(self.cantidad)

        if self.producto is not None and hasattr(self.producto, "inventario"):
            return self.producto.inventario.liberar_stock(self.cantidad)

        return "No existe inventario"

    def descontar_stock(self):
        if self.producto_tienda is not None:
            return self.producto_tienda.descontar_stock(self.cantidad)

        if self.producto is not None and hasattr(self.producto, "inventario"):
            return self.producto.inventario.descontar_stock(self.cantidad)

        return "No existe inventario"

    def save(self, *args, **kwargs):
        if self.producto_tienda is not None:
            self.producto = self.producto_tienda.producto

            if self.precio_unitario == 0:
                self.precio_unitario = self.producto_tienda.precio_venta

        elif self.producto is not None and self.precio_unitario == 0:
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
            return self.pedido.pagar_y_descontar_stock()
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
        return self.pedido.obtener_empresa_proveedora()

    def obtener_tienda(self):
        return self.pedido.obtener_nombre_tienda()

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
