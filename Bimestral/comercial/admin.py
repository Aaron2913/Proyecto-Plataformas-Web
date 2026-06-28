from django.contrib import admin

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

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(Vendedor)
admin.site.register(Producto)
admin.site.register(Inventario)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Pago)
admin.site.register(Factura)
admin.site.register(Comision)
admin.site.register(Suscripcion)
admin.site.register(Calificacion)
admin.site.register(Notificacion)
admin.site.register(Tutorial)