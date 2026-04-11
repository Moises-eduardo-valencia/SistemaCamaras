# SistemaCamaras

Sistema web para el registro, inventario y control de mantenimientos de cámaras de seguridad, desarrollado con Django 6.0.

## Tecnologías

- **Backend:** Django 6.0.3, Python 3.12
- **Base de datos:** SQLite (desarrollo)
- **Frontend:** Tailwind CSS (via CDN)
- **Gestor de paquetes:** uv
- **Tareas programadas:** django-apscheduler
- **Autenticación:** Django Auth integrado

## Funcionalidades

### Cámaras
- Registro, edición y eliminación de cámaras
- Listado con búsqueda y filtros
- Cada cámara tiene un token UUID único para acceso sin login
- Acción masiva desde el admin para cambiar empresa
- Generación de etiquetas QR imprimibles por empresa para registro rápido de mantenimiento

### Mantenimientos
- Registro de mantenimientos por cámara (limpieza de lente, interior, verificación de conector y alimentación)
- Cálculo automático de próxima fecha hábil
- **Mantenimiento rápido:** formulario público accesible via QR o NFC, sin necesidad de login (`/mantenimientos/rapido/<token>/`)
- Historial de mantenimientos por cámara

### Reportes automáticos por correo
- Reporte mensual de inventario de cámaras (día 1 del mes, 8:00 AM)
- Reporte mensual de mantenimientos del mes anterior (día 1 del mes, 8:30 AM)
- Gestión de destinatarios por empresa con activación/desactivación individual

## Estructura del proyecto

```
SistemaCamaras/
├── Proyecto/               # Configuración principal de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── camaras/                # App de gestión de cámaras
│   ├── models.py           # Modelo Camara (empresa, nombre, modelo, serie, IP, MAC, token)
│   ├── views.py            # CRUD de cámaras
│   ├── forms.py            # CamaraForm con validación de MAC
│   ├── admin.py            # Acciones: cambiar empresa, generar etiquetas QR
│   └── templates/
├── mantenimientos/         # App de mantenimientos
│   ├── models.py           # Modelos Mantenimiento y DestinatarioReporte
│   ├── views.py            # CRUD + mantenimiento rápido (público) + destinatarios
│   ├── forms.py
│   ├── scheduler.py        # Tareas programadas con APScheduler
│   ├── reports.py          # Envío de reportes por correo
│   └── templates/
├── templates/
│   └── base.html           # Template base con navbar y Tailwind CSS
├── manage.py
├── pyproject.toml
└── .env                    # Variables de entorno (no commitear)
```

## Requisitos previos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Instalación

1. Clonar el repositorio:

```bash
git clone <url-del-repositorio>
cd SistemaCamaras
```

2. Instalar dependencias:

```bash
uv sync
```

3. Configurar variables de entorno — crear `.env` en la raíz:

```
SECRET_KEY=tu-clave-secreta
EMAIL_HOST_USER=correo@dominio.com
EMAIL_HOST_PASSWORD=contraseña-sendgrid
```

4. Aplicar migraciones:

```bash
uv run python manage.py migrate
```

5. Crear superusuario:

```bash
uv run python manage.py createsuperuser
```

6. Ejecutar el servidor de desarrollo:

```bash
uv run python manage.py runserver
```

## URLs principales

| URL | Descripción |
|---|---|
| `/` | Redirige a `/camaras/` |
| `/camaras/` | Listado de cámaras |
| `/camaras/registrar/` | Registrar nueva cámara |
| `/mantenimientos/` | Historial de mantenimientos |
| `/mantenimientos/registrar/` | Registrar mantenimiento |
| `/mantenimientos/rapido/<token>/` | Formulario público via QR/NFC |
| `/mantenimientos/destinatarios/` | Gestión de destinatarios de reportes |
| `/admin/` | Panel de administración Django |

## Uso del QR / NFC

Desde el panel admin (`/admin/camaras/camara/`):

1. Selecciona una o más cámaras
2. Elige la acción **"Generar etiquetas QR por empresa"**
3. Imprime la hoja — cada etiqueta incluye el QR y las instrucciones
4. El técnico escanea el QR (o acerca la etiqueta NFC) para acceder al formulario de mantenimiento sin necesidad de login

## Licencia

Este proyecto es de uso privado.
