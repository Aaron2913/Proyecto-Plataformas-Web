# Proyecto Bimestral - Plataforma Web Comercial

Este repositorio contiene una aplicación web desarrollada con **Python**, **Django** y **Django REST Framework**. El sistema permite gestionar usuarios tipo **empresa** y **vendedor**, productos, inventarios, pedidos, pagos, facturas, comisiones, suscripciones, calificaciones, notificaciones y tutoriales.

El proyecto incluye vistas HTML para la interacción del usuario y servicios web REST protegidos mediante autenticación por **Token**.

---

## Tecnologías utilizadas

- Python
- Django 6.0.6
- Django REST Framework
- SQLite
- HTML/CSS
- Token Authentication

---

## Estructura principal del repositorio

```text
Proyecto-Plataformas-Web-main/
│
├── Bimestral/
│   ├── manage.py
│   ├── db.sqlite3
│   ├── requirements.txt
│   ├── proyecto_bimestral/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── comercial/
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── models.py
│       ├── serializers.py
│       ├── urls.py
│       ├── views.py
│       ├── migrations/
│       ├── static/
│       └── templates/
│
└── PRESENTACION-1BM/
    ├── Proyecto_Bimestral.pdf
    └── Proyecto_Bimestral.zip
```

La carpeta que se debe ejecutar es:

```text
Bimestral/
```

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/Aaron2913/Proyecto-Plataformas-Web.git
```

Ejemplo:

```bash
cd Proyecto-Plataformas-Web
```

---

## 2. Entrar al proyecto Django

```bash
cd Bimestral
```

Verificar que en esta carpeta exista el archivo:

```text
ls 
manage.py
```

---

## 3. Crear entorno virtual

En Windows:

```bash
py -m venv venv
venv\Scripts\activate
```

En Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Instalar dependencias

El proyecto incluye un archivo `requirements.txt`. Para instalar las dependencias ejecutar:

```bash
py -m pip install -r requirements.txt
```

Si el comando `py` no funciona, usar:

```bash
python -m pip install -r requirements.txt
```

Dependencias principales:

```text
Django==6.0.6
djangorestframework
Flask
requests
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2025.3
```

---

## 5. Aplicar migraciones

Aunque el repositorio incluye `db.sqlite3`, se recomienda ejecutar las migraciones para verificar que la base de datos esté actualizada:

```bash
py manage.py makemigrations
py manage.py migrate
```

Si se usa `python`:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Crear superusuario para el panel de administración

Si se desea ingresar al panel `/admin/`, crear un superusuario:

```bash
py manage.py createsuperuser
```

Luego ingresar usuario, correo y contraseña solicitados por consola.

---

## 7. Crear token para consumir la API REST

La API REST está protegida con autenticación por token. Para generar un token, ejecutar:

```bash
py manage.py drf_create_token NOMBRE_DEL_USUARIO
```

Ejemplo:

```bash
py manage.py drf_create_token admin
```

Si ya existe un usuario llamado `Admin`, también se puede generar con:

```bash
py manage.py drf_create_token Admin
```

El comando devolverá un token similar a:

```text
Generated token 123456789abcdef...
```

Ese token se debe usar en las peticiones a la API con el encabezado:

```text
Authorization: Token TOKEN_GENERADO
```

Ejemplo con `curl`:

```bash
curl -H "Authorization: Token TOKEN_GENERADO" http://127.0.0.1:8000/api/productos/
```

---

## 8. Ejecutar el servidor Django

```bash
py manage.py runserver
```

El proyecto se levantará en:

```text
http://127.0.0.1:8000/
```

---

## 9. Rutas principales del sistema

### Inicio y autenticación

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/login/
http://127.0.0.1:8000/logout/
http://127.0.0.1:8000/admin/
```

### Registro de usuarios

```text
http://127.0.0.1:8000/registro/empresa/
http://127.0.0.1:8000/registro/vendedor/
```

### Vistas para empresa

```text
http://127.0.0.1:8000/empresa/inicio/
http://127.0.0.1:8000/empresa/productos/
http://127.0.0.1:8000/empresa/productos/crear/
http://127.0.0.1:8000/empresa/inventario/
http://127.0.0.1:8000/empresa/inventario/crear/
http://127.0.0.1:8000/empresa/pedidos/
```

### Vistas para vendedor

```text
http://127.0.0.1:8000/vendedor/inicio/
http://127.0.0.1:8000/vendedor/catalogo/
http://127.0.0.1:8000/vendedor/pedidos/
http://127.0.0.1:8000/vendedor/pedidos/crear/
http://127.0.0.1:8000/vendedor/detalle/crear/
http://127.0.0.1:8000/vendedor/pagos/
http://127.0.0.1:8000/vendedor/pagos/crear/
http://127.0.0.1:8000/vendedor/tutoriales/
```

### Resumen

```text
http://127.0.0.1:8000/resumen/
```

---

## 10. Rutas de la API REST

La API se encuentra en:

```text
http://127.0.0.1:8000/api/
```

Endpoints disponibles:

```text
http://127.0.0.1:8000/api/usuarios/
http://127.0.0.1:8000/api/empresas/
http://127.0.0.1:8000/api/vendedores/
http://127.0.0.1:8000/api/productos/
http://127.0.0.1:8000/api/inventarios/
http://127.0.0.1:8000/api/pedidos/
http://127.0.0.1:8000/api/detalles-pedido/
http://127.0.0.1:8000/api/pagos/
http://127.0.0.1:8000/api/facturas/
http://127.0.0.1:8000/api/comisiones/
http://127.0.0.1:8000/api/suscripciones/
http://127.0.0.1:8000/api/calificaciones/
http://127.0.0.1:8000/api/notificaciones/
http://127.0.0.1:8000/api/tutoriales/
```

Nota: Si se abre una ruta de la API directamente desde el navegador y aparece:

```text
401 Unauthorized
Authentication credentials were not provided.
```

esto es normal, ya que la API requiere token de autenticación.

---

## 11. Usuarios de prueba de la aplicación

El archivo `db.sqlite3` incluido contiene datos de prueba. Para ingresar por la pantalla de login de la aplicación se pueden usar usuarios registrados en la base de datos, por ejemplo:

### Usuario tipo empresa

```text
Correo: empresa@gmail.com
Contraseña: 12345
```

### Usuario tipo vendedor

```text
Correo: jzco2000@gmail.com
Contraseña: 12345678
```

También se pueden crear nuevos usuarios desde:

```text
http://127.0.0.1:8000/registro/empresa/
http://127.0.0.1:8000/registro/vendedor/
```

---

## 12. Panel de administración

Para ingresar al panel administrativo:

```text
http://127.0.0.1:8000/admin/
```

Si no se conoce la contraseña de un usuario administrador existente, crear uno nuevo con:

```bash
py manage.py createsuperuser
```
