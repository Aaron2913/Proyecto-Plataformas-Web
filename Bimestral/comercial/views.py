from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import F

from rest_framework import viewsets

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
from .models import Factura
from .models import Comision
from .models import Suscripcion
from .models import Calificacion
from .models import Notificacion
from .models import Tutorial

from .forms import LoginForm
from .forms import UsuarioEmpresaForm
from .forms import RegistroEmpresaForm
from .forms import UsuarioTenderoForm
from .forms import RegistroTiendaForm
from .forms import UsuarioVendedorForm
from .forms import RegistroVendedorForm
from .forms import ProductoEmpresaForm
from .forms import InventarioEmpresaForm
from .forms import PedidoVendedorForm
from .forms import DetallePedidoVendedorForm
from .forms import PagoVendedorForm
from .forms import PedidoEmpresaTenderoForm
from .forms import DetallePedidoEmpresaTenderoForm
from .forms import PagoPedidoEmpresaTenderoForm

from .serializers import UsuarioSerializer
from .serializers import EmpresaSerializer
from .serializers import VendedorSerializer
from .serializers import TiendaSerializer
from .serializers import ProductoSerializer
from .serializers import InventarioSerializer
from .serializers import ProductoTiendaSerializer
from .serializers import PedidoSerializer
from .serializers import DetallePedidoSerializer
from .serializers import PagoSerializer
from .serializers import PedidoEmpresaSerializer
from .serializers import DetallePedidoEmpresaSerializer
from .serializers import PagoPedidoEmpresaSerializer
from .serializers import FacturaSerializer
from .serializers import ComisionSerializer
from .serializers import SuscripcionSerializer
from .serializers import CalificacionSerializer
from .serializers import NotificacionSerializer
from .serializers import TutorialSerializer


# ==========================
# LOGIN Y SESIÓN
# ==========================


def login_usuario(request):
    mensaje = ""

    if request.method == "POST":
        formulario = LoginForm(request.POST)

        if formulario.is_valid():
            usuario = Usuario.autenticar(
                formulario.cleaned_data["correo"],
                formulario.cleaned_data["contrasena"],
            )

            if usuario is not None:
                usuario.guardar_en_sesion(request)
                return redirect("inicio")

            mensaje = "Correo o contraseña incorrectos"
    else:
        formulario = LoginForm()

    return render(
        request,
        "comercial/login.html",
        {
            "formulario": formulario,
            "mensaje": mensaje,
        },
    )


def cerrar_sesion(request):
    request.session.flush()
    return redirect("login")


def inicio(request):
    redireccion = Usuario.obtener_redireccion_acceso(request)

    if redireccion:
        return redirect(redireccion)

    usuario = Usuario.obtener_usuario_sesion(request)
    return redirect(usuario.obtener_inicio_por_rol())


# ==========================
# REGISTROS
# ==========================


def registro_empresa(request):
    if request.method == "POST":
        formulario_usuario = UsuarioEmpresaForm(request.POST)
        formulario_empresa = RegistroEmpresaForm(request.POST)

        if formulario_usuario.is_valid() and formulario_empresa.is_valid():
            Empresa.registrar_desde_formularios(formulario_usuario, formulario_empresa)
            return redirect("login")
    else:
        formulario_usuario = UsuarioEmpresaForm()
        formulario_empresa = RegistroEmpresaForm()

    return render(
        request,
        "comercial/registro_empresa.html",
        {
            "formulario_usuario": formulario_usuario,
            "formulario_empresa": formulario_empresa,
        },
    )


def registro_tendero(request):
    if request.method == "POST":
        formulario_usuario = UsuarioTenderoForm(request.POST)
        formulario_tienda = RegistroTiendaForm(request.POST)

        if formulario_usuario.is_valid() and formulario_tienda.is_valid():
            Tienda.registrar_desde_formularios(formulario_usuario, formulario_tienda)
            return redirect("login")
    else:
        formulario_usuario = UsuarioTenderoForm()
        formulario_tienda = RegistroTiendaForm()

    return render(
        request,
        "comercial/registro_tendero.html",
        {
            "formulario_usuario": formulario_usuario,
            "formulario_tienda": formulario_tienda,
        },
    )


def registro_vendedor(request):
    if request.method == "POST":
        formulario_usuario = UsuarioVendedorForm(request.POST)
        formulario_vendedor = RegistroVendedorForm(request.POST)

        if formulario_usuario.is_valid() and formulario_vendedor.is_valid():
            Vendedor.registrar_desde_formularios(formulario_usuario, formulario_vendedor)
            return redirect("login")
    else:
        formulario_usuario = UsuarioVendedorForm()
        formulario_vendedor = RegistroVendedorForm()

    return render(
        request,
        "comercial/registro_vendedor.html",
        {
            "formulario_usuario": formulario_usuario,
            "formulario_vendedor": formulario_vendedor,
        },
    )


# ==========================
# VISTAS DE EMPRESA
# ==========================


def inicio_empresa(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "EMPRESA")

    if redireccion:
        return redirect(redireccion)

    empresa = Empresa.obtener_actual_desde_request(request)
    return render(request, "comercial/inicio_empresa.html", empresa.obtener_resumen_dashboard())


def productos_empresa(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "EMPRESA")

    if redireccion:
        return redirect(redireccion)

    empresa = Empresa.obtener_actual_desde_request(request)
    return render(request, "comercial/productos_empresa.html", empresa.obtener_contexto_productos())


def crear_producto_empresa(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "EMPRESA")

    if redireccion:
        return redirect(redireccion)

    empresa = Empresa.obtener_actual_desde_request(request)

    if request.method == "POST":
        formulario = ProductoEmpresaForm(request.POST)

        if formulario.is_valid():
            empresa.crear_producto(formulario)
            return redirect("productos_empresa")
    else:
        formulario = ProductoEmpresaForm()

    return render(
        request,
        "comercial/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Registrar producto",
        },
    )


def inventario_empresa(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "EMPRESA")

    if redireccion:
        return redirect(redireccion)

    empresa = Empresa.obtener_actual_desde_request(request)
    return render(request, "comercial/inventario_empresa.html", empresa.obtener_contexto_inventarios())


def crear_inventario_empresa(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "EMPRESA")

    if redireccion:
        return redirect(redireccion)

    empresa = Empresa.obtener_actual_desde_request(request)
    mensaje = ""

    if request.method == "POST":
        formulario = InventarioEmpresaForm(request.POST)
        formulario = empresa.configurar_formulario_inventario(formulario)

        if formulario.is_valid():
            try:
                empresa.crear_inventario(formulario)
                return redirect("inventario_empresa")
            except ValueError as error:
                mensaje = str(error)
    else:
        formulario = InventarioEmpresaForm()
        formulario = empresa.configurar_formulario_inventario(formulario)

    return render(
        request,
        "comercial/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Registrar inventario",
            "mensaje": mensaje,
        },
    )


def tiendas_empresa(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "EMPRESA")

    if redireccion:
        return redirect(redireccion)

    empresa = Empresa.obtener_actual_desde_request(request)
    return render(request, "comercial/tiendas_empresa.html", empresa.obtener_contexto_tiendas())


def pedidos_empresa(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "EMPRESA")

    if redireccion:
        return redirect(redireccion)

    empresa = Empresa.obtener_actual_desde_request(request)
    return render(request, "comercial/pedidos_empresa.html", empresa.obtener_contexto_pedidos_recibidos())


def confirmar_pedido_empresa(request, pedido_id):
    redireccion = Usuario.obtener_redireccion_acceso(request, "EMPRESA")

    if redireccion:
        return redirect(redireccion)

    if request.method == "POST":
        empresa = Empresa.obtener_actual_desde_request(request)
        empresa.ejecutar_accion_pedido_recibido(pedido_id, "CONFIRMAR")

    return redirect("pedidos_empresa")


def preparar_pedido_empresa(request, pedido_id):
    redireccion = Usuario.obtener_redireccion_acceso(request, "EMPRESA")

    if redireccion:
        return redirect(redireccion)

    if request.method == "POST":
        empresa = Empresa.obtener_actual_desde_request(request)
        empresa.ejecutar_accion_pedido_recibido(pedido_id, "PREPARAR")

    return redirect("pedidos_empresa")


def entregar_pedido_empresa(request, pedido_id):
    redireccion = Usuario.obtener_redireccion_acceso(request, "EMPRESA")

    if redireccion:
        return redirect(redireccion)

    if request.method == "POST":
        empresa = Empresa.obtener_actual_desde_request(request)
        empresa.ejecutar_accion_pedido_recibido(pedido_id, "ENTREGAR")

    return redirect("pedidos_empresa")



def confirmar_pedido_empresa(request, pedido_id):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = Empresa.obtener_por_usuario_id(request.session.get("usuario_id"))
    pedido = get_object_or_404(PedidoEmpresa, id=pedido_id, empresa=empresa)

    if request.method == "POST":
        pedido.confirmar_pedido()

    return redirect("pedidos_empresa")


def preparar_pedido_empresa(request, pedido_id):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = Empresa.obtener_por_usuario_id(request.session.get("usuario_id"))
    pedido = get_object_or_404(PedidoEmpresa, id=pedido_id, empresa=empresa)

    if request.method == "POST":
        pedido.pasar_a_preparacion()

    return redirect("pedidos_empresa")


def entregar_pedido_empresa(request, pedido_id):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = Empresa.obtener_por_usuario_id(request.session.get("usuario_id"))
    pedido = get_object_or_404(PedidoEmpresa, id=pedido_id, empresa=empresa)

    if request.method == "POST":
        pedido.entregar_pedido()

    return redirect("pedidos_empresa")


# ==========================
# VISTAS DE TENDERO
# ==========================


def inicio_tendero(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    tienda = Tienda.obtener_actual_desde_request(request)
    return render(request, "comercial/inicio_tendero.html", tienda.obtener_resumen_dashboard())


def productos_tendero(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    tienda = Tienda.obtener_actual_desde_request(request)
    return render(request, "comercial/productos_tendero.html", tienda.obtener_contexto_productos_tienda())


def crear_producto_tendero(request):
<<<<<<< HEAD
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")
=======
    """Ruta antigua conservada: ahora el abastecimiento se realiza mediante órdenes."""
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "TENDERO":
        return redirect("inicio")

    return redirect("crear_pedido_empresa_tendero")


def catalogo_empresas_tendero(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "TENDERO":
        return redirect("inicio")

    tienda = Tienda.obtener_por_usuario_id(request.session.get("usuario_id"))
    productos = Producto.objects.filter(
        empresa__estado_validacion="APROBADA",
        disponible=True,
        inventario__stock_actual__gt=F("inventario__stock_reservado"),
    ).select_related("empresa", "inventario").order_by(
        "empresa__razon_social", "nombre"
    )

    return render(
        request,
        "comercial/catalogo_empresas_tendero.html",
        {"tienda": tienda, "productos": productos},
    )


def pedidos_empresa_tendero(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "TENDERO":
        return redirect("inicio")

    tienda = Tienda.obtener_por_usuario_id(request.session.get("usuario_id"))
    pedidos = tienda.listar_pedidos_a_empresas()

    return render(
        request,
        "comercial/pedidos_empresa_tendero.html",
        {"tienda": tienda, "pedidos": pedidos},
    )


def crear_pedido_empresa_tendero(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "TENDERO":
        return redirect("inicio")

    tienda = Tienda.obtener_por_usuario_id(request.session.get("usuario_id"))

    if request.method == "POST":
        formulario = PedidoEmpresaTenderoForm(request.POST)
        formulario = tienda.configurar_formulario_pedido_empresa(formulario)

        if formulario.is_valid():
            tienda.crear_pedido_empresa(formulario)
            return redirect("pedidos_empresa_tendero")
    else:
        formulario = PedidoEmpresaTenderoForm()
        formulario = tienda.configurar_formulario_pedido_empresa(formulario)

    return render(
        request,
        "comercial/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Crear pedido a una empresa",
            "ayuda": "Selecciona primero la empresa proveedora. Después agrega sus productos a la orden.",
        },
    )


def crear_detalle_empresa_tendero(request):
    if not request.session.get("usuario_id"):
        return redirect("login")
>>>>>>> 8f5e627ad741458334eb4c9b1ee198ad463e0a30

    if redireccion:
        return redirect(redireccion)

    return redirect("crear_pedido_empresa_tendero")


def catalogo_empresas_tendero(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    tienda = Tienda.obtener_actual_desde_request(request)
    return render(request, "comercial/catalogo_empresas_tendero.html", tienda.obtener_contexto_catalogo_empresas())


def pedidos_empresa_tendero(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    tienda = Tienda.obtener_actual_desde_request(request)
    return render(request, "comercial/pedidos_empresa_tendero.html", tienda.obtener_contexto_pedidos_empresa())


def crear_pedido_empresa_tendero(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    tienda = Tienda.obtener_actual_desde_request(request)

    if request.method == "POST":
        formulario = PedidoEmpresaTenderoForm(request.POST)
        formulario = tienda.configurar_formulario_pedido_empresa(formulario)

        if formulario.is_valid():
            tienda.crear_pedido_empresa(formulario)
            return redirect("pedidos_empresa_tendero")
    else:
        formulario = PedidoEmpresaTenderoForm()
        formulario = tienda.configurar_formulario_pedido_empresa(formulario)

    return render(
        request,
        "comercial/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Crear pedido a una empresa",
            "ayuda": "Selecciona primero la empresa proveedora. Después agrega sus productos a la orden.",
        },
    )


def crear_detalle_empresa_tendero(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    tienda = Tienda.obtener_actual_desde_request(request)
    mensaje = ""

    if request.method == "POST":
        formulario = DetallePedidoEmpresaTenderoForm(request.POST)
        formulario = tienda.configurar_formulario_detalle_empresa(formulario)

        if formulario.is_valid():
            try:
                tienda.agregar_detalle_empresa(formulario)
                return redirect("pedidos_empresa_tendero")
            except ValueError as error:
                mensaje = str(error)
    else:
        formulario = DetallePedidoEmpresaTenderoForm()
        formulario = tienda.configurar_formulario_detalle_empresa(formulario)

    return render(
        request,
        "comercial/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Agregar producto al pedido de empresa",
            "mensaje": mensaje,
            "ayuda": "El producto debe pertenecer a la empresa seleccionada. La cantidad quedará reservada en su inventario.",
        },
    )


def pagos_empresa_tendero(request):
<<<<<<< HEAD
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    tienda = Tienda.obtener_actual_desde_request(request)
    return render(request, "comercial/pagos_empresa_tendero.html", tienda.obtener_contexto_pagos_empresa())


def crear_pago_empresa_tendero(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    tienda = Tienda.obtener_actual_desde_request(request)
=======
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "TENDERO":
        return redirect("inicio")

    tienda = Tienda.obtener_por_usuario_id(request.session.get("usuario_id"))
    pagos = tienda.listar_pagos_a_empresas()

    return render(
        request,
        "comercial/pagos_empresa_tendero.html",
        {"tienda": tienda, "pagos": pagos},
    )


def crear_pago_empresa_tendero(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "TENDERO":
        return redirect("inicio")

    tienda = Tienda.obtener_por_usuario_id(request.session.get("usuario_id"))
>>>>>>> 8f5e627ad741458334eb4c9b1ee198ad463e0a30
    mensaje = ""

    if request.method == "POST":
        formulario = PagoPedidoEmpresaTenderoForm(request.POST)
        formulario = tienda.configurar_formulario_pago_empresa(formulario)

        if formulario.is_valid():
            try:
                tienda.registrar_pago_empresa(formulario)
                return redirect("pagos_empresa_tendero")
            except ValueError as error:
                mensaje = str(error)
    else:
        formulario = PagoPedidoEmpresaTenderoForm()
        formulario = tienda.configurar_formulario_pago_empresa(formulario)

    return render(
        request,
        "comercial/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Pagar pedido a empresa",
            "mensaje": mensaje,
            "ayuda": "Al pagar, la orden se cierra y el stock reservado se descuenta del inventario de la empresa.",
        },
    )


def cancelar_pedido_empresa_tendero(request, pedido_id):
<<<<<<< HEAD
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    if request.method == "POST":
        tienda = Tienda.obtener_actual_desde_request(request)
=======
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "TENDERO":
        return redirect("inicio")

    tienda = Tienda.obtener_por_usuario_id(request.session.get("usuario_id"))

    if request.method == "POST":
>>>>>>> 8f5e627ad741458334eb4c9b1ee198ad463e0a30
        tienda.cancelar_pedido_empresa(pedido_id)

    return redirect("pedidos_empresa_tendero")


def detalle_pedido_empresa_tendero(request, pedido_id):
<<<<<<< HEAD
    redireccion = Usuario.obtener_redireccion_acceso(request)

    if redireccion:
        return redirect(redireccion)

    contexto = PedidoEmpresa.obtener_contexto_detalle_por_usuario(
        request.session.get("usuario_id"),
        request.session.get("tipo_usuario"),
        pedido_id,
    )

    if contexto is None:
        return redirect("inicio")

    return render(request, "comercial/detalle_pedido_empresa.html", contexto)
=======
    usuario_id = request.session.get("usuario_id")
    tipo_usuario = request.session.get("tipo_usuario")

    if not usuario_id:
        return redirect("login")

    pedido = get_object_or_404(
        PedidoEmpresa.objects.select_related("tienda__usuario", "empresa__usuario"),
        id=pedido_id,
    )

    if tipo_usuario == "TENDERO":
        if pedido.tienda.usuario_id != usuario_id:
            return redirect("inicio")
        volver_url = reverse("pedidos_empresa_tendero")
        titulo_origen = "Mis pedidos a empresas"
    elif tipo_usuario == "EMPRESA":
        if pedido.empresa.usuario_id != usuario_id:
            return redirect("inicio")
        volver_url = reverse("pedidos_empresa")
        titulo_origen = "Pedidos recibidos"
    else:
        return redirect("inicio")

    detalles = pedido.detalles.select_related("producto__empresa").all()
    pago = PagoPedidoEmpresa.objects.filter(pedido=pedido).first()

    return render(
        request,
        "comercial/detalle_pedido_empresa.html",
        {
            "pedido": pedido,
            "detalles": detalles,
            "pago": pago,
            "volver_url": volver_url,
            "titulo_origen": titulo_origen,
        },
    )
>>>>>>> 8f5e627ad741458334eb4c9b1ee198ad463e0a30


def pedidos_tendero(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    tienda = Tienda.obtener_actual_desde_request(request)
    return render(request, "comercial/pedidos_tendero.html", tienda.obtener_contexto_pedidos_recibidos())


def confirmar_pedido_tendero(request, pedido_id):
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    if request.method == "POST":
        tienda = Tienda.obtener_actual_desde_request(request)
        tienda.confirmar_pedido(pedido_id)

    return redirect("pedidos_tendero")


def preparar_pedido_tendero(request, pedido_id):
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    if request.method == "POST":
        tienda = Tienda.obtener_actual_desde_request(request)
        tienda.pasar_pedido_a_preparacion(pedido_id)

    return redirect("pedidos_tendero")


def entregar_pedido_tendero(request, pedido_id):
    redireccion = Usuario.obtener_redireccion_acceso(request, "TENDERO")

    if redireccion:
        return redirect(redireccion)

    if request.method == "POST":
        tienda = Tienda.obtener_actual_desde_request(request)
        tienda.entregar_pedido(pedido_id)

    return redirect("pedidos_tendero")


# ==========================
# VISTAS DE VENDEDOR / DELIVERY
# ==========================


def inicio_vendedor(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "VENDEDOR")

    if redireccion:
        return redirect(redireccion)

    vendedor = Vendedor.obtener_actual_desde_request(request)
    return render(request, "comercial/inicio_vendedor.html", vendedor.obtener_resumen_dashboard())


def catalogo_vendedor(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "VENDEDOR")

    if redireccion:
        return redirect(redireccion)

    vendedor = Vendedor.obtener_actual_desde_request(request)
    return render(request, "comercial/catalogo_vendedor.html", vendedor.obtener_contexto_catalogo())


def pedidos_vendedor(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "VENDEDOR")

    if redireccion:
        return redirect(redireccion)

    vendedor = Vendedor.obtener_actual_desde_request(request)
    return render(request, "comercial/pedidos_vendedor.html", vendedor.obtener_contexto_pedidos())


def detalle_pedido(request, pedido_id):
    redireccion = Usuario.obtener_redireccion_acceso(request)

    if redireccion:
        return redirect(redireccion)

    contexto = Pedido.obtener_contexto_detalle_por_usuario(
        request.session.get("usuario_id"),
        request.session.get("tipo_usuario"),
        pedido_id,
    )

    if contexto is None:
        return redirect("inicio")

    return render(request, "comercial/detalle_pedido.html", contexto)


def detalle_pedido(request, pedido_id):
    """Muestra los productos reales de una orden y valida el acceso por rol."""
    usuario_id = request.session.get("usuario_id")
    tipo_usuario = request.session.get("tipo_usuario")

    if not usuario_id:
        return redirect("login")

    pedido = get_object_or_404(
        Pedido.objects.select_related(
            "vendedor__usuario",
            "tienda__usuario",
        ),
        id=pedido_id,
    )

    detalles = pedido.detalles.select_related(
        "producto",
        "producto_tienda__producto__empresa",
        "producto_tienda__tienda",
    ).all()

    if tipo_usuario == "VENDEDOR":
        if pedido.vendedor.usuario_id != usuario_id:
            return redirect("inicio")
        volver_url = reverse("pedidos_vendedor")
        titulo_origen = "Mis pedidos"

    elif tipo_usuario == "TENDERO":
        if pedido.tienda is None or pedido.tienda.usuario_id != usuario_id:
            return redirect("inicio")
        volver_url = reverse("pedidos_tendero")
        titulo_origen = "Pedidos recibidos"

    elif tipo_usuario == "EMPRESA":
        empresa = Empresa.obtener_por_usuario_id(usuario_id)
        detalles = detalles.filter(producto_tienda__producto__empresa=empresa)

        if not detalles.exists():
            return redirect("inicio")

        volver_url = reverse("pedidos_empresa")
        titulo_origen = "Pedidos recibidos"

    else:
        return redirect("inicio")

    total_detalles = sum(detalle.subtotal for detalle in detalles)
    pago = Pago.objects.filter(pedido=pedido).first()

    informacion_template = {
        "pedido": pedido,
        "detalles": detalles,
        "total_detalles": total_detalles,
        "pago": pago,
        "volver_url": volver_url,
        "titulo_origen": titulo_origen,
        "es_empresa": tipo_usuario == "EMPRESA",
    }

    return render(request, "comercial/detalle_pedido.html", informacion_template)


def crear_pedido_vendedor(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "VENDEDOR")

    if redireccion:
        return redirect(redireccion)

    vendedor = Vendedor.obtener_actual_desde_request(request)

    if request.method == "POST":
        formulario = PedidoVendedorForm(request.POST)

        if formulario.is_valid():
            vendedor.crear_pedido(formulario)
            return redirect("pedidos_vendedor")
    else:
        formulario = PedidoVendedorForm()

    return render(
        request,
        "comercial/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Crear pedido a una tienda",
        },
    )


def crear_detalle_vendedor(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "VENDEDOR")

    if redireccion:
        return redirect(redireccion)

    vendedor = Vendedor.obtener_actual_desde_request(request)
    mensaje = ""
    ayuda = "Solo aparecen pedidos abiertos. Si la compra anterior ya fue pagada, primero crea un pedido nuevo."

    if request.method == "POST":
        formulario = DetallePedidoVendedorForm(request.POST)
        formulario = vendedor.configurar_formulario_detalle(formulario)

        if formulario.is_valid():
            try:
                vendedor.agregar_detalle_pedido(formulario)
                return redirect("pedidos_vendedor")
            except ValueError as error:
                mensaje = str(error)
    else:
        formulario = DetallePedidoVendedorForm()
        formulario = vendedor.configurar_formulario_detalle(formulario)

<<<<<<< HEAD
    return render(
        request,
        "comercial/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Agregar producto de tienda al pedido",
            "mensaje": mensaje,
            "ayuda": ayuda,
        },
    )
=======
    informacion_template = {
        "formulario": formulario,
        "titulo": "Agregar producto de tienda al pedido",
        "mensaje": mensaje,
        "ayuda": ayuda,
    }

    return render(request, "comercial/formulario.html", informacion_template)
>>>>>>> 8f5e627ad741458334eb4c9b1ee198ad463e0a30


def cancelar_pedido_vendedor(request, pedido_id):
    redireccion = Usuario.obtener_redireccion_acceso(request, "VENDEDOR")

    if redireccion:
        return redirect(redireccion)

    if request.method == "POST":
        vendedor = Vendedor.obtener_actual_desde_request(request)
        vendedor.cancelar_pedido(pedido_id)

    return redirect("pedidos_vendedor")


def pagos_vendedor(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "VENDEDOR")

    if redireccion:
        return redirect(redireccion)

    vendedor = Vendedor.obtener_actual_desde_request(request)
    return render(request, "comercial/pagos_vendedor.html", vendedor.obtener_contexto_pagos())


def crear_pago_vendedor(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "VENDEDOR")

    if redireccion:
        return redirect(redireccion)

    vendedor = Vendedor.obtener_actual_desde_request(request)
    mensaje = ""

    if request.method == "POST":
        formulario = PagoVendedorForm(request.POST)
        formulario = vendedor.configurar_formulario_pago(formulario)

        if formulario.is_valid():
            try:
                vendedor.registrar_pago(formulario)
                return redirect("pagos_vendedor")
            except ValueError as error:
                mensaje = str(error)
    else:
        formulario = PagoVendedorForm()
        formulario = vendedor.configurar_formulario_pago(formulario)

<<<<<<< HEAD
    return render(
        request,
        "comercial/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Pagar pedido",
            "mensaje": mensaje,
            "ayuda": "El monto debe coincidir con el total. Al guardar, la orden quedará pagada y cerrada para nuevos productos.",
        },
    )
=======
    informacion_template = {
        "formulario": formulario,
        "titulo": "Pagar pedido",
        "mensaje": mensaje,
        "ayuda": "El monto debe coincidir con el total. Al guardar, la orden quedará pagada y cerrada para nuevos productos.",
    }

    return render(request, "comercial/formulario.html", informacion_template)
>>>>>>> 8f5e627ad741458334eb4c9b1ee198ad463e0a30


def tutoriales_vendedor(request):
    redireccion = Usuario.obtener_redireccion_acceso(request, "VENDEDOR")

    if redireccion:
        return redirect(redireccion)

    vendedor = Vendedor.obtener_actual_desde_request(request)
    return render(request, "comercial/tutoriales_vendedor.html", vendedor.obtener_contexto_tutoriales())


# ==========================
# RESUMEN JSON
# ==========================

<<<<<<< HEAD
=======
def resumen(request):
    datos = {
        "usuarios": Usuario.objects.count(),
        "empresas": Empresa.objects.count(),
        "tenderos": Tienda.objects.count(),
        "vendedores": Vendedor.objects.count(),
        "productos_empresa": Producto.objects.count(),
        "inventarios_empresa": Inventario.objects.count(),
        "productos_tienda": ProductoTienda.objects.count(),
        "pedidos": Pedido.objects.count(),
        "detalles_pedido": DetallePedido.objects.count(),
        "pagos": Pago.objects.count(),
        "pedidos_empresa": PedidoEmpresa.objects.count(),
        "detalles_pedido_empresa": DetallePedidoEmpresa.objects.count(),
        "pagos_pedido_empresa": PagoPedidoEmpresa.objects.count(),
        "facturas": Factura.objects.count(),
        "comisiones": Comision.objects.count(),
        "suscripciones": Suscripcion.objects.count(),
        "calificaciones": Calificacion.objects.count(),
        "notificaciones": Notificacion.objects.count(),
        "tutoriales": Tutorial.objects.count(),
    }
>>>>>>> 8f5e627ad741458334eb4c9b1ee198ad463e0a30

def resumen(request):
    return JsonResponse(Usuario.obtener_resumen_sistema())


# ==========================
# API PARA FLASK
# ==========================


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer


class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer


class ProductoTiendaViewSet(viewsets.ModelViewSet):
    queryset = ProductoTienda.objects.all()
    serializer_class = ProductoTiendaSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer


class PedidoEmpresaViewSet(viewsets.ModelViewSet):
    queryset = PedidoEmpresa.objects.all()
    serializer_class = PedidoEmpresaSerializer


class DetallePedidoEmpresaViewSet(viewsets.ModelViewSet):
    queryset = DetallePedidoEmpresa.objects.all()
    serializer_class = DetallePedidoEmpresaSerializer


class PagoPedidoEmpresaViewSet(viewsets.ModelViewSet):
    queryset = PagoPedidoEmpresa.objects.all()
    serializer_class = PagoPedidoEmpresaSerializer


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer


class ComisionViewSet(viewsets.ModelViewSet):
    queryset = Comision.objects.all()
    serializer_class = ComisionSerializer


class SuscripcionViewSet(viewsets.ModelViewSet):
    queryset = Suscripcion.objects.all()
    serializer_class = SuscripcionSerializer


class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer


class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer


class TutorialViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
