# Operaciones CRUD

## Objetivo

Permitir administrar la información principal del sistema Biblioteca Córdoba

---

# Usuarios

## Crear

Permite registrar nuevos usuarios

## Leer

Permite visualizar todos los usuarios registrados

## Actualizar

Permite modificar la información de un usuario existente

## Eliminar

Permite eliminar usuarios registrados

---

# Libros

## Crear

Permite registrar nuevos libros

## Leer

Permite visualizar los libros registrados

## Actualizar

Permite modificar la información de los libros

## Eliminar

Permite eliminar libros registrados

---

# Búsquedas

## Usuarios

El sistema permite buscar usuarios por:

- Nombre
- Apellido
- DNI
- Email

## Libros

El sistema permite buscar libros por:

- Título
- Autor
- Categoría

## Préstamos

El sistema permite buscar préstamos por:

- Nombre del usuario
- Apellido del usuario
- DNI
- Título del libro
- Autor

---

# Filtros

## Libros

Los libros pueden filtrarse por:

- Disponible
- Prestado
- Reservado

## Préstamos

Los préstamos pueden filtrarse por:

- Activo
- Devuelto

---

# Tecnologías utilizadas

- Django
- ModelForm
- Templates
- Bootstrap
- SQLite

---

# Estado

Las operaciones CRUD principales de usuarios y libros están implementadas y probadas

Las operaciones de gestión de préstamos y devoluciones también se encuentran implementadas y probadas

## Referencia de documentación consolidada

Para el alcance vigente, contrastar este apunte con `requisitos_funcionales.md`, `requisitos_no_funcionales.md`, `casos_de_uso.md` y `../docs/base_de_datos.md`. La regla actual exige bloquear el cambio manual del estado de un libro con préstamo activo.
