# Listados de Información

## Objetivo

Permitir visualizar y consultar los registros almacenados en la base
de datos.

---

# Listado de Usuarios

Permite visualizar:

- DNI
- Nombre
- Apellido
- Teléfono
- Email

También permite buscar por:

- Nombre
- Apellido
- DNI
- Email

---

# Listado de Libros

Permite visualizar:

- Título
- Autor
- Categoría
- Editorial
- Año
- Estado

Permite:

- Buscar libros.
- Filtrar por estado.
- Ordenar alfabéticamente por título.

---

# Listado de Préstamos

Permite visualizar:

- Usuario
- Libro
- Fecha de préstamo
- Fecha de devolución
- Estado

Permite:

- Buscar por usuario.
- Buscar por libro.
- Filtrar por estado.
- Registrar devoluciones de préstamos activos.

---

# Implementación

Los listados utilizan QuerySets de Django.

Los resultados son enviados a los templates mediante contextos.

Los templates utilizan bucles para mostrar los registros en tablas HTML.

---

# Estado

Los listados de usuarios, libros y préstamos se encuentran implementados.

## Referencia de documentación consolidada

Para el alcance vigente, contrastar este apunte con `requisitos_funcionales.md`, `requisitos_no_funcionales.md`, `casos_de_uso.md` y `../docs/base_de_datos.md`. La regla actual exige bloquear el cambio manual del estado de un libro con préstamo activo.
