# Módulo Préstamos

## Objetivo

Permitir registrar y administrar los préstamos de libros realizados por los usuarios de la biblioteca

## Información del préstamo

Cada préstamo contiene:

- Usuario
- Libro
- Fecha de préstamo
- Fecha de devolución
- Estado

## Estados

Los préstamos pueden encontrarse en los siguientes estados:

- Activo
- Devuelto

Al registrar un préstamo nuevo, su estado inicial es:

**Activo**

## Relaciones

Un usuario puede realizar múltiples préstamos

Un libro puede participar en múltiples préstamos a lo largo del tiempo

Cada préstamo pertenece a:

- Un usuario
- Un libro

Estas relaciones se implementan mediante `ForeignKey` en Django

## Registro de préstamos

Para registrar un préstamo el sistema solicita:

1. Usuario
2. Libro

La fecha de préstamo se genera automáticamente

## Reglas de negocio

Antes de registrar un préstamo se verifica que:

- El usuario exista
- El libro exista
- El libro se encuentre Disponible
- No exista otro préstamo Activo para el mismo libro

No se permite prestar nuevamente un libro que ya se encuentra Prestado

## Flujo de préstamo

```text
Usuario
   ↓
Seleccionar libro
   ↓
Libro Disponible
   ↓
Registrar préstamo
   ↓
Préstamo Activo
   ↓
Libro Prestado

## Referencia de documentación consolidada

Para el alcance vigente, contrastar este apunte con `requisitos_funcionales.md`, `requisitos_no_funcionales.md`, `casos_de_uso.md` y `../docs/base_de_datos.md`. La regla actual exige bloquear el cambio manual del estado de un libro con préstamo activo.
