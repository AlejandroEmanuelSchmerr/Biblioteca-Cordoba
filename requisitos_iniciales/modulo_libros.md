# Módulo Libros

## Objetivo

Administrar los libros registrados en el sistema Biblioteca Córdoba.

---

## Funcionalidades implementadas

El módulo permite:

- Registrar libros.
- Listar libros.
- Editar libros.
- Eliminar libros.
- Buscar libros.
- Filtrar libros por estado.
- Ordenar libros alfabéticamente por título.

---

## Información almacenada

Cada libro contiene:

- ID del libro
- Título
- Autor
- Editorial
- Año
- Categoría
- Estado

---

## Estados disponibles

Los libros pueden encontrarse en los siguientes estados:

- Disponible
- Prestado
- Reservado

Al crear un libro nuevo, su estado inicial es:

**Disponible**

---

## Búsquedas

El sistema permite buscar libros mediante:

- Título
- Autor
- Categoría

La búsqueda utiliza coincidencias parciales mediante `icontains`.

---

## Filtros

El listado permite filtrar libros por:

- Disponible
- Prestado
- Reservado

---

## Ordenamiento

Los libros se muestran ordenados alfabéticamente por título.

---

## Flujo

1. Registrar un libro.
2. El libro comienza como Disponible.
3. Visualizar el listado.
4. Buscar o filtrar libros.
5. Editar la información cuando sea necesario.
6. Eliminar el libro cuando corresponda.

---

## Integración con préstamos

Cuando un libro disponible es prestado:

```text
Disponible
↓
Préstamo
↓
Prestado

## Referencia de documentación consolidada

Para el alcance vigente, contrastar este apunte con `requisitos_funcionales.md`, `requisitos_no_funcionales.md`, `casos_de_uso.md` y `../docs/base_de_datos.md`. La regla actual exige bloquear el cambio manual del estado de un libro con préstamo activo.
