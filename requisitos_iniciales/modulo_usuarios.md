# Módulo Usuarios

## Objetivo

Permitir administrar los usuarios registrados en el sistema Biblioteca Córdoba

## Funcionalidades implementadas

- Crear usuarios
- Listar usuarios
- Editar usuarios
- Eliminar usuarios
- Buscar usuarios
- Buscar por nombre
- Buscar por apellido
- Buscar por DNI
- Buscar por email

## Información almacenada

Cada usuario contiene:

- DNI
- Nombre
- Apellido
- Teléfono
- Email

## Validaciones

El DNI debe contener únicamente números

Durante la edición el DNI no puede modificarse porque funciona como clave primaria

## Tecnologías utilizadas

- Django
- ModelForm
- Templates
- Bootstrap
- SQLite

## Flujo

1. Crear un usuario
2. Visualizar la lista
3. Buscar usuarios
4. Editar la información
5. Eliminar un usuario cuando corresponda

## Estado

Módulo funcional y probado mediante pruebas automáticas y pruebas manuales# Módulo Usuarios

## Objetivo

Permitir administrar los usuarios registrados en el sistema Biblioteca Córdoba

## Funcionalidades implementadas

- Crear usuarios
- Listar usuarios
- Editar usuarios
- Eliminar usuarios
- Buscar usuarios
- Buscar por nombre
- Buscar por apellido
- Buscar por DNI
- Buscar por email

## Información almacenada

Cada usuario contiene:

- DNI
- Nombre
- Apellido
- Teléfono
- Email

## Validaciones

El DNI debe contener únicamente números

Durante la edición el DNI no puede modificarse porque funciona como clave primaria

## Tecnologías utilizadas

- Django
- ModelForm
- Templates
- Bootstrap
- SQLite

## Flujo

1. Crear un usuario
2. Visualizar la lista
3. Buscar usuarios
4. Editar la información
5. Eliminar un usuario cuando corresponda

## Estado

Módulo funcional y probado mediante pruebas automáticas y pruebas manuales

## Referencia de documentación consolidada

Para el alcance vigente, contrastar este apunte con `requisitos_funcionales.md`, `requisitos_no_funcionales.md`, `casos_de_uso.md` y `../docs/base_de_datos.md`. La regla actual exige bloquear el cambio manual del estado de un libro con préstamo activo.
