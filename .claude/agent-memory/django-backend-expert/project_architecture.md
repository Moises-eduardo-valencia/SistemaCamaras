---
name: project_architecture
description: Arquitectura general del proyecto SistemaCamaras — apps, modelos, rutas y decisiones de diseño
type: project
---

## Stack
- Django 6.0.3, Python 3.12, SQLite
- Virtualenv: `.venvProyCamara/`
- Locale: `es-mx`, timezone: `America/Mexico_City`
- Sin DRF — vistas function-based, templates HTML bare (sin base template ni static files aún)

## Apps

### camaras
Modelo `Camara`: empresa, nombre, modelo, serie, ip (GenericIPAddressField), mac, created_at, updated_at.
`__str__` retorna `nombre`. Rutas montadas en `/camaras/`.
Última migración: `0002_camara_created_at_camara_updated_at`.

### mantenimientos
Implementada en 2026-03-11. Modelo `Mantenimiento` con FK a `Camara` (CASCADE), campos booleanos de tareas, DateField para fechas, TextField para observaciones, timestamps auto.
`__str__` retorna `f"{self.camara.nombre} - {self.fecha_mantenimiento}"`.
Meta: `ordering=['-fecha_mantenimiento']`.
Rutas base en `/mantenimientos/` (el agente de integración/frontend las monta en `Proyecto/urls.py`).
Migración: `0001_initial.py` — depende de `('camaras', '0002_camara_created_at_camara_updated_at')`.

## Convenciones
- Todas las vistas protegidas con `@login_required`
- `messages.success` / `messages.error` para feedback al usuario
- `select_related('camara')` en queries de lista para evitar N+1
- `get_object_or_404` en vistas de detalle/edición/eliminación
- Formularios de fecha con widget `DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')`
- Campo camara en formulario usa `CamaraChoiceField` (subclase de `ModelChoiceField`) con `label_from_instance` → `"empresa — nombre (serie)"`

## Responsabilidades por agente
- Este agente (backend): modelos, vistas, formularios, admin, migraciones
- Agente frontend/integración: templates, `settings.py` (INSTALLED_APPS), `Proyecto/urls.py` (include de URLs de cada app)
