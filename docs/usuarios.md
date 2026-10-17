# Usuarios de Biblioteca

## Objetivo

Documentar la entidad `Usuario` utilizada por Biblioteca Córdoba para representar a las personas registradas en la biblioteca.

## Usuario de biblioteca

El Usuario de biblioteca no es una cuenta de autenticación de Django.

Representa a una persona que puede recibir préstamos y cuyos datos son administrados por el bibliotecario.

## Datos

- DNI
- Nombre
- Apellido
- Teléfono
- Correo electrónico

El DNI es la clave primaria de la entidad.

## Funcionalidades actuales

El bibliotecario puede:

- Registrar usuarios
- Consultar usuarios
- Buscar usuarios por nombre, apellido, DNI o email
- Editar usuarios
- Eliminar usuarios

## Validación del DNI

El formulario verifica que el DNI contenga únicamente números.

Durante la edición, el DNI queda deshabilitado porque funciona como clave primaria.

## Usuario del sistema

El acceso a Biblioteca Córdoba se realiza mediante el sistema de autenticación de Django.

La cuenta de Django se utiliza exclusivamente para controlar el acceso al sistema y no reemplaza a la entidad `Usuario` de la biblioteca.

## Funcionalidades futuras

No se implementa actualmente un portal independiente para que el Usuario de biblioteca inicie sesión, consulte sus préstamos o consulte su historial. Esas funciones pueden incorporarse en una ampliación posterior.
