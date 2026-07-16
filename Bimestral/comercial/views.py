from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse

from rest_framework import viewsets

from .models import Usuario
from .models import Empresa
from .models import Vendedor
from .models import Producto
from .models import Inventario
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
from .forms import UsuarioVendedorForm
from .forms import RegistroVendedorForm
from .forms import ProductoEmpresaForm
from .forms import InventarioEmpresaForm
from .forms import PedidoVendedorForm
from .forms import DetallePedidoVendedorForm
from .forms import PagoVendedorForm

from .serializers import UsuarioSerializer
from .serializers import EmpresaSerializer
from .serializers import VendedorSerializer
from .serializers import ProductoSerializer
from .serializers import InventarioSerializer
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

            usuario = Usuario.objects.filter(
                correo=correo,
                contrasena=contrasena,
                estado="ACTIVO"
            ).first()

            if usuario is not None:
                request.session["usuario_id"] = usuario.id
                request.session["usuario_nombre"] = usuario.nombre
                request.session["tipo_usuario"] = usuario.tipo_usuario

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
    if not request.session.get("usuario_id"):
        return redirect("login")

    tipo_usuario = request.session.get("tipo_usuario")

    if tipo_usuario == "EMPRESA":
        return redirect("inicio_empresa")

    if tipo_usuario == "VENDEDOR":
        return redirect("inicio_vendedor")

    return redirect("login")


# ==========================
# REGISTROS
# ==========================

def registro_empresa(request):
    if request.method == "POST":
        formulario_usuario = UsuarioEmpresaForm(request.POST)
        formulario_empresa = RegistroEmpresaForm(request.POST)

        if formulario_usuario.is_valid() and formulario_empresa.is_valid():
            usuario = formulario_usuario.save(commit=False)
            usuario.estado = "ACTIVO"
            usuario.tipo_usuario = "EMPRESA"
            usuario.save()

            empresa = formulario_empresa.save(commit=False)
            empresa.usuario = usuario
            empresa.estado_validacion = "PENDIENTE"
            empresa.save()

            return redirect("login")
    else:
        formulario_usuario = UsuarioEmpresaForm()
        formulario_empresa = RegistroEmpresaForm()

    informacion_template = {
        "formulario_usuario": formulario_usuario,
        "formulario_empresa": formulario_empresa
    }

    return render(request, "comercial/registro_empresa.html", informacion_template)


def registro_vendedor(request):
    if request.method == "POST":
        formulario_usuario = UsuarioVendedorForm(request.POST)
        formulario_vendedor = RegistroVendedorForm(request.POST)

        if formulario_usuario.is_valid() and formulario_vendedor.is_valid():
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
# FUNCIONES DE APOYO
# ==========================

def obtener_empresa_actual(request):
    usuario_id = request.session.get("usuario_id")
    usuario = Usuario.objects.get(id=usuario_id)
    empresa = Empresa.objects.get(usuario=usuario)

    return empresa


def obtener_vendedor_actual(request):
    usuario_id = request.session.get("usuario_id")
    usuario = Usuario.objects.get(id=usuario_id)
    vendedor = Vendedor.objects.get(usuario=usuario)

    return vendedor


# ==========================
# VISTAS DE EMPRESA
# ==========================

def inicio_empresa(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = obtener_empresa_actual(request)

    total_productos = Producto.objects.filter(empresa=empresa).count()
    total_inventarios = Inventario.objects.filter(producto__empresa=empresa).count()
    total_pedidos = Pedido.objects.filter(empresa=empresa).count()

    informacion_template = {
        "empresa": empresa,
        "total_productos": total_productos,
        "total_inventarios": total_inventarios,
        "total_pedidos": total_pedidos,
    }

    return render(request, "comercial/inicio_empresa.html", informacion_template)


def productos_empresa(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = obtener_empresa_actual(request)
    productos = Producto.objects.filter(empresa=empresa)

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

    empresa = obtener_empresa_actual(request)

    if request.method == "POST":
        formulario = ProductoEmpresaForm(request.POST)

        if formulario.is_valid():
            producto = formulario.save(commit=False)
            producto.empresa = empresa
            producto.save()

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

    empresa = obtener_empresa_actual(request)
    inventarios = Inventario.objects.filter(producto__empresa=empresa)

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

    empresa = obtener_empresa_actual(request)

    if request.method == "POST":
        formulario = InventarioEmpresaForm(request.POST)
        formulario.fields["producto"].queryset = Producto.objects.filter(empresa=empresa)

        if formulario.is_valid():
            formulario.save()
            return redirect("inventario_empresa")
    else:
        formulario = InventarioEmpresaForm()
        formulario.fields["producto"].queryset = Producto.objects.filter(empresa=empresa)

    informacion_template = {
        "formulario": formulario,
        "titulo": "Registrar inventario"
    }

    return render(request, "comercial/formulario.html", informacion_template)


def pedidos_empresa(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "EMPRESA":
        return redirect("inicio")

    empresa = obtener_empresa_actual(request)
    pedidos = Pedido.objects.filter(empresa=empresa)

    informacion_template = {
        "empresa": empresa,
        "pedidos": pedidos
    }

    return render(request, "comercial/pedidos_empresa.html", informacion_template)


# ==========================
# VISTAS DE VENDEDOR
# ==========================

def inicio_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = obtener_vendedor_actual(request)

    total_pedidos = Pedido.objects.filter(vendedor=vendedor).count()
    total_pagos = Pago.objects.filter(pedido__vendedor=vendedor).count()
    total_productos = Producto.objects.filter(disponible=True).count()

    informacion_template = {
        "vendedor": vendedor,
        "total_pedidos": total_pedidos,
        "total_pagos": total_pagos,
        "total_productos": total_productos,
    }

    return render(request, "comercial/inicio_vendedor.html", informacion_template)


def catalogo_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    productos = Producto.objects.filter(disponible=True)

    informacion_template = {
        "productos": productos
    }

    return render(request, "comercial/catalogo_vendedor.html", informacion_template)


def pedidos_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = obtener_vendedor_actual(request)
    pedidos = Pedido.objects.filter(vendedor=vendedor)

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

    vendedor = obtener_vendedor_actual(request)

    if request.method == "POST":
        formulario = PedidoVendedorForm(request.POST)

        if formulario.is_valid():
            pedido = formulario.save(commit=False)
            pedido.vendedor = vendedor
            pedido.estado = "PENDIENTE"
            pedido.subtotal = 0
            pedido.total = 0
            pedido.save()

            return redirect("pedidos_vendedor")
    else:
        formulario = PedidoVendedorForm()

    informacion_template = {
        "formulario": formulario,
        "titulo": "Crear pedido"
    }

    return render(request, "comercial/formulario.html", informacion_template)


def crear_detalle_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = obtener_vendedor_actual(request)

    if request.method == "POST":
        formulario = DetallePedidoVendedorForm(request.POST)
        formulario.fields["pedido"].queryset = Pedido.objects.filter(vendedor=vendedor)

        if formulario.is_valid():
            formulario.save()
            return redirect("pedidos_vendedor")
    else:
        formulario = DetallePedidoVendedorForm()
        formulario.fields["pedido"].queryset = Pedido.objects.filter(vendedor=vendedor)

    informacion_template = {
        "formulario": formulario,
        "titulo": "Agregar producto al pedido"
    }

    return render(request, "comercial/formulario.html", informacion_template)


def pagos_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = obtener_vendedor_actual(request)
    pagos = Pago.objects.filter(pedido__vendedor=vendedor)

    informacion_template = {
        "pagos": pagos
    }

    return render(request, "comercial/pagos_vendedor.html", informacion_template)


def crear_pago_vendedor(request):
    if not request.session.get("usuario_id"):
        return redirect("login")

    if request.session.get("tipo_usuario") != "VENDEDOR":
        return redirect("inicio")

    vendedor = obtener_vendedor_actual(request)

    if request.method == "POST":
        formulario = PagoVendedorForm(request.POST)
        formulario.fields["pedido"].queryset = Pedido.objects.filter(vendedor=vendedor)

        if formulario.is_valid():
            pago = formulario.save()

            if pago.estado_pago == "APROBADO":
                pago.validar_pago()

            return redirect("pagos_vendedor")
    else:
        formulario = PagoVendedorForm()
        formulario.fields["pedido"].queryset = Pedido.objects.filter(vendedor=vendedor)

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
        "vendedores": Vendedor.objects.count(),
        "productos": Producto.objects.count(),
        "inventarios": Inventario.objects.count(),
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


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer


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