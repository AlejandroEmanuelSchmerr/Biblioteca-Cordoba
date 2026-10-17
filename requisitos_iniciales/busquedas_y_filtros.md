# Búsquedas y Filtros

## Objetivo

Facilitar la localización de información dentro de Biblioteca Córdoba.

## Búsqueda de usuarios

El sistema permite buscar mediante:

- Nombre
- Apellido
- DNI
- Email

La búsqueda utiliza coincidencias parciales mediante `icontains`.

## Búsqueda de libros

El sistema permite buscar mediante:

- Título
- Autor
- Categoría

La búsqueda utiliza coincidencias parciales mediante `icontains`.

## Filtros de libros

Los libros pueden filtrarse por:

- Disponible
- Prestado
- Reservado

## Ordenamiento de libros

Los libros se muestran ordenados alfabéticamente por título.

## Búsqueda de préstamos

El sistema permite buscar mediante:

- Nombre del usuario
- Apellido del usuario
- DNI del usuario
- Título del libro
- Autor del libro

## Filtros de préstamos

Los préstamos pueden filtrarse por:

- Activo
- Devuelto

## Tecnologías utilizadas

- Django QuerySet
- `filter()`
- `order_by()`
- `icontains`
- `Q`

## Estado

Las búsquedas, filtros y ordenamientos descritos se encuentran implementados en las vistas correspondientes.

## Referencia de documentación consolidada

Para el alcance vigente, contrastar este apunte con `requisitos_funcionales.md`, `requisitos_no_funcionales.md`, `casos_de_uso.md` y `../docs/base_de_datos.md`. La regla actual exige bloquear el cambio manual del estado de un libro con préstamo activo.
