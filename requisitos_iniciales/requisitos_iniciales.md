# Sistema Biblioteca Córdoba

## Objetivo

Desarrollar un sistema web para administrar una biblioteca, permitiendo gestionar libros, usuarios y préstamos de manera digital.

## Alcance de la versión implementada

La versión actual está orientada al **Bibliotecario**, quien utiliza el sistema para realizar las operaciones diarias de la biblioteca.

El proyecto también posee la entidad `Usuario`, que representa a las personas registradas en la biblioteca y que pueden recibir préstamos.

La entidad Usuario no representa actualmente una cuenta de acceso al sistema.

## Problemas que resuelve

- Evita pérdidas de información
- Facilita la gestión de préstamos
- Permite buscar información rápidamente
- Permite saber qué usuario tiene un libro
- Facilita el control de devoluciones
- Mantiene un historial de préstamos

## Información almacenada

### Usuarios de biblioteca

- Nombre
- Apellido
- DNI
- Correo electrónico
- Teléfono

### Libros

- Título
- Autor
- Editorial
- Año
- Categoría
- Estado

### Préstamos

- Usuario
- Libro
- Fecha de préstamo
- Fecha de devolución
- Estado

## Funcionalidades implementadas

- Registrar usuarios
- Modificar usuarios
- Eliminar usuarios
- Buscar usuarios
- Registrar libros
- Modificar libros
- Eliminar libros
- Buscar libros
- Filtrar libros por estado
- Registrar préstamos
- Registrar devoluciones
- Buscar préstamos
- Filtrar préstamos
- Iniciar sesión
- Cerrar sesión
- Mostrar estadísticas básicas en el panel principal

## Tecnologías utilizadas

- Python
- Django
- HTML
- Bootstrap
- SQLite
- Git
- GitHub

## Funcionalidades futuras

Podrán agregarse posteriormente perfiles y funciones específicas para usuarios de biblioteca, además de roles diferenciados mediante grupos y permisos de Django.

## Referencia de documentación consolidada

Para el alcance vigente, contrastar este apunte con `requisitos_funcionales.md`, `requisitos_no_funcionales.md`, `casos_de_uso.md` y `../docs/base_de_datos.md`. La regla actual exige bloquear el cambio manual del estado de un libro con préstamo activo.
