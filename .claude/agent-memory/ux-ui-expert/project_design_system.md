---
name: Design System — SistemaCamaras
description: CSS framework, paleta de colores, tipografia y convenciones visuales confirmadas en el proyecto
type: project
---

## Framework y herramientas

- Tailwind CSS via CDN (`https://cdn.tailwindcss.com`) — no hay build process todavia
- Templates Django con herencia desde `templates/base.html`
- No hay JavaScript propio; interacciones son navegacion nativa

## Paleta de colores confirmada

- Encabezado de tabla y navbar: `bg-gray-700` / `bg-gray-800`
- Accion primaria (CTA): `bg-blue-600 hover:bg-blue-700`
- Accion destructiva: `text-red-500 hover:text-red-700`
- Accion editar: `text-blue-600 hover:text-blue-800`
- Accion QR/NFC: `text-purple-600 hover:text-purple-800`
- Fondo de pagina: `bg-gray-100`
- Cards y tablas: `bg-white shadow rounded-lg`
- Empty state: `text-gray-500` sobre `bg-white`

## Convenciones de layout

- Max width del contenido: `max-w-6xl mx-auto px-4` (definido en base.html `<main>`)
- Header de pagina: `flex justify-between items-center mb-6` con h1 + boton CTA a la derecha
- Tablas: siempre envueltas en `overflow-x-auto`, con `w-full` y `shadow rounded-lg overflow-hidden`
- Padding de celdas: `px-4 py-3` para datos, `text-sm` para contenido
- Datos tecnicos (IP, MAC, Serie): `font-mono`
- Nombre/identificador principal: `font-medium`

## Accesibilidad — gaps sistematicos identificados

- `<html lang="es">` en base.html — deberia ser `lang="es-MX"` para locale del proyecto
- Touch targets de iconos de accion (~20px) — requieren `p-2 -m-2` para llegar a ~36px
- `<th>` sin atributo `scope` en ningun template
- Emojis ✅❌ usados sin texto alternativo en lista_mantenimientos.html

## Estructura de vistas de lista

Patron consistente en ambas listas:
1. Header row (h1 + CTA button)
2. `{% if data %}` tabla `{% else %}` empty state `{% endif %}`
- No hay paginacion todavia
- No hay busqueda ni filtros (en desarrollo)
