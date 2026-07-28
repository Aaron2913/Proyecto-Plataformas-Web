from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse

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
from .forms import ProductoTiendaForm
from .forms import PedidoVendedorForm
from .forms import DetallePedidoVendedorForm
from .forms import PagoVendedorForm

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
            correo = formulario.cleaned_data["correo"]
            contrasena = formulario.cleaned_data["contrasena"]

            usuario = Usuario.autenticar(correo, contrasena)

            if usuario is not None:
                usuario.guardar_en_sesion(request)
                return redirect("inicio")
            else:
                mensaje = "Correo o contraseña incorrectos"
    else:
        formulario = LoginForm()

    informacion_template = {
        "formulario": formulario,
        "mensaje": mensaje
    }

    return render(request, "comercial/login.html", informacion_template)


def cerrar_sesion(request):
    request.session.flush()
    return redirect("login")


def inicio(request):
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return redirect("login")

    usuario = Usuario.obtener_por_id(usuario_id)
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

    informacion_template = {
        "formulario_usuario": formulario_usuario,
        "formulario_empresa": formulario_empresa
    }

    return render(request, "comercial/registro_empresa.html", informacion_template)


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

    informacion_template = {
        "formulario_usuario": formulario_usuario,
        "formulario_tienda": formulario_tienda
    }

    return render(request, "comercial/registro_tendero.html", informacion_template)


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

    informacion_template = {
        "formulario_usuario": formulario_usuario,
        "formulario_vendedor": formulario_vendedor
    }

    return render(request, "comercial/registro_vendedor.html", informacion_template)


# ==========================
# VISTAS DE EMPRESA
# ==========================

def inicio_empresa(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = Empresa.obtener_por_usuario_id(request.session.get("usuario_id"))
    informacion_template = empresa.obtener_resumen_dashboard()

    return render(request, "comercial/inicio_empresa.html", informacion_template)


def productos_empresa(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = Empresa.obtener_por_usuario_id(request.session.get("usuario_id"))
    productos = empresa.listar_productos()

    informacion_template = {
        "empresa": empresa,
        "productos": productos
    }

    return render(request, "comercial/productos_empresa.html", informacion_template)


def crear_producto_empresa(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = Empresa.obtener_por_usuario_id(request.session.get("usuario_id"))

    if request.method == "POST":
        formulario = ProductoEmpresaForm(request.POST)

        if formulario.is_valid():
            empresa.crear_producto(formulario)
            return redirect("productos_empresa")
    else:
        formulario = ProductoEmpresaForm()

    informacion_template = {
        "formulario": formulario,
        "titulo": "Registrar producto"
    }

    return render(request, "comercial/formulario.html", informacion_template)


def inventario_empresa(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = Empresa.obtener_por_usuario_id(request.session.get("usuario_id"))
    inventarios = empresa.listar_inventarios()

    informacion_template = {
        "empresa": empresa,
        "inventarios": inventarios
    }

    return render(request, "comercial/inventario_empresa.html", informacion_template)


def crear_inventario_empresa(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = Empresa.obtener_por_usuario_id(request.session.get("usuario_id"))

    if request.method == "POST":
        formulario = InventarioEmpresaForm(request.POST)
        formulario = empresa.configurar_formulario_inventario(formulario)

        if formulario.is_valid():
            formulario.save()
            return redirect("inventario_empresa")
    else:
        formulario = InventarioEmpresaForm()
        formulario = empresa.configurar_formulario_inventario(formulario)

    informacion_template = {
        "formulario": formulario,
        "titulo": "Registrar inventario"
    }

    return render(request, "comercial/formulario.html", informacion_template)


def tiendas_empresa(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = Empresa.obtener_por_usuario_id(request.session.get("usuario_id"))
    tiendas = empresa.listar_tiendas()

    informacion_template = {
        "empresa": empresa,
        "tiendas": tiendas
    }

    return render(request, "comercial/tiendas_empresa.html", informacion_template)


def pedidos_empresa(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = Empresa.obtener_por_usuario_id(request.session.get("usuario_id"))
    pedidos = empresa.listar_pedidos_recibidos()

    informacion_template = {
        "empresa": empresa,
        "pedidos": pedidos
    }

    return render(request, "comercial/pedidos_empresa.html", informacion_template)


# ==========================
# VISTAS DE TENDERO
# ==========================

def inicio_tendero(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "TENDERO":
        return redirect("inicio")

    tienda = Tienda.obtener_por_usuario_id(request.session.get("usuario_id"))
    informacion_template = tienda.obtener_resumen_dashboard()

    return render(request, "comercial/inicio_tendero.html", informacion_template)


def productos_tendero(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "TENDERO":
        return redirect("inicio")

    tienda = Tienda.obtener_por_usuario_id(request.session.get("usuario_id"))
    productos_tienda = tienda.listar_productos_tienda()

    informacion_template = {
        "tienda": tienda,
        "productos_tienda": productos_tienda
    }

    return render(request, "comercial/productos_tendero.html", informacion_template)


def crear_producto_tendero(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "TENDERO":
        return redirect("inicio")

    tienda = Tienda.obtener_por_usuario_id(request.session.get("usuario_id"))

    if request.method == "POST":
        formulario = ProductoTiendaForm(request.POST)
        formulario = tienda.configurar_formulario_producto_tienda(formulario)

        if formulario.is_valid():
            tienda.crear_producto_tienda(formulario)
            return redirect("productos_tendero")
    else:
        formulario = ProductoTiendaForm()
        formulario = tienda.configurar_formulario_producto_tienda(formulario)

    informacion_template = {
        "formulario": formulario,
        "titulo": "Agregar producto a la tienda"
    }

    return render(request, "comercial/formulario.html", informacion_template)


def pedidos_tendero(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "TENDERO":
        return redirect("inicio")

    tienda = Tienda.obtener_por_usuario_id(request.session.get("usuario_id"))
    pedidos = tienda.listar_pedidos_recibidos()

    informacion_template = {
        "tienda": tienda,
        "pedidos": pedidos
    }

    return render(request, "comercial/pedidos_tendero.html", informacion_template)


# ==========================
# VISTAS DE VENDEDOR / DELIVERY
# ==========================

def inicio_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = Vendedor.obtener_por_usuario_id(request.session.get("usuario_id"))
    informacion_template = vendedor.obtener_resumen_dashboard()

    return render(request, "comercial/inicio_vendedor.html", informacion_template)


def catalogo_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = Vendedor.obtener_por_usuario_id(request.session.get("usuario_id"))
    productos_tienda = vendedor.listar_catalogo()

    informacion_template = {
        "productos_tienda": productos_tienda
    }

    return render(request, "comercial/catalogo_vendedor.html", informacion_template)


def pedidos_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = Vendedor.obtener_por_usuario_id(request.session.get("usuario_id"))
    pedidos = vendedor.listar_pedidos()

    informacion_template = {
        "vendedor": vendedor,
        "pedidos": pedidos
    }

    return render(request, "comercial/pedidos_vendedor.html", informacion_template)


def crear_pedido_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = Vendedor.obtener_por_usuario_id(request.session.get("usuario_id"))

    if request.method == "POST":
        formulario = PedidoVendedorForm(request.POST)

        if formulario.is_valid():
            vendedor.crear_pedido(formulario)
            return redirect("pedidos_vendedor")
    else:
        formulario = PedidoVendedorForm()

    informacion_template = {
        "formulario": formulario,
        "titulo": "Crear pedido a una tienda"
    }

    return render(request, "comercial/formulario.html", informacion_template)


def crear_detalle_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = Vendedor.obtener_por_usuario_id(request.session.get("usuario_id"))

    if request.method == "POST":
        formulario = DetallePedidoVendedorForm(request.POST)
        formulario = vendedor.configurar_formulario_detalle(formulario)

        if formulario.is_valid():
            formulario.save()
            return redirect("pedidos_vendedor")
    else:
        formulario = DetallePedidoVendedorForm()
        formulario = vendedor.configurar_formulario_detalle(formulario)

    informacion_template = {
        "formulario": formulario,
        "titulo": "Agregar producto de tienda al pedido"
    }

    return render(request, "comercial/formulario.html", informacion_template)


def pagos_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = Vendedor.obtener_por_usuario_id(request.session.get("usuario_id"))
    pagos = vendedor.listar_pagos()

    informacion_template = {
        "pagos": pagos
    }

    return render(request, "comercial/pagos_vendedor.html", informacion_template)


def crear_pago_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = Vendedor.obtener_por_usuario_id(request.session.get("usuario_id"))

    if request.method == "POST":
        formulario = PagoVendedorForm(request.POST)
        formulario = vendedor.configurar_formulario_pago(formulario)

        if formulario.is_valid():
            pago = formulario.save()
            pago.validar_pago()
            return redirect("pagos_vendedor")
    else:
        formulario = PagoVendedorForm()
        formulario = vendedor.configurar_formulario_pago(formulario)

    informacion_template = {
        "formulario": formulario,
        "titulo": "Registrar pago"
    }

    return render(request, "comercial/formulario.html", informacion_template)


def tutoriales_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    tutoriales = Tutorial.objects.all()

    informacion_template = {
        "tutoriales": tutoriales
    }

    return render(request, "comercial/tutoriales_vendedor.html", informacion_template)


# ==========================
# RESUMEN JSON
# ==========================

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
        "facturas": Factura.objects.count(),
        "comisiones": Comision.objects.count(),
        "suscripciones": Suscripcion.objects.count(),
        "calificaciones": Calificacion.objects.count(),
        "notificaciones": Notificacion.objects.count(),
        "tutoriales": Tutorial.objects.count(),
    }

    return JsonResponse(datos)


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
