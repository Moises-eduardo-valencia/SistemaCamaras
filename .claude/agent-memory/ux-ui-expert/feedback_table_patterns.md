---
name: Patrones para tablas densas y filtros tipo chip
description: Decisiones de diseno validadas para tablas con muchas columnas y filtros de empresa en SistemaCamaras
type: feedback
---

## Filtros tipo chip/pill para empresa

Usar `<a href="?empresa=X">` con `rounded-full` — no botones ni JS.

**Why:** Hace los filtros bookmarkables y shareables. El backend lee `request.GET.get('empresa')`. Sin JS necesario.

**How to apply:** Colocar la barra de chips ENTRE el header (h1 + CTA) y la tabla, como banda propia con `mb-4`. Chip activo usa `bg-gray-700 text-white` (consistente con encabezado de tabla). Chip inactivo usa `bg-white border border-gray-300`.

## Columnas de checks booleanos en tablas

Usar badges SVG circulares (`bg-green-100` / `bg-red-100`) en lugar de emojis ✅❌.

**Why:** Los emojis tienen renderizado inconsistente entre OS y no son accesibles sin texto alternativo. Los badges SVG son consistentes, accesibles con `aria-label`, y visualmente mas limpios.

**How to apply:** `<span class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-green-100">` con SVG checkmark/X adentro. Reducir padding de columna a `px-2` para ahorrar espacio horizontal.

## Agrupacion de columnas con colspan

Cuando hay 4+ columnas relacionadas (como los 4 checks de mantenimiento), usar `<thead>` con dos filas: super-encabezado con `colspan` y sub-encabezados con iconos SVG + `<span class="sr-only">` para accesibilidad. Esto reduce el ancho total significativamente.

## Empty state diferenciado

Dos estados visuales distintos: "sin datos en BD" vs "filtro sin resultados". El segundo incluye siempre un link de recuperacion ("ver todos"). El primero no lo necesita.

**Why:** Nielsen heuristica #9 — ayudar al usuario a recuperarse de errores. Sin diferenciacion, el usuario no sabe si el sistema esta vacio o si su filtro es muy restrictivo.

## Touch targets en iconos de accion

Usar `p-2 -m-2 rounded` en el `<a>` que contiene el SVG de accion (editar/eliminar). Expande area tactil a ~36px sin cambiar layout visual.
