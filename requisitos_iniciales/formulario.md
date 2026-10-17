# Formularios

## Objetivo

Permitir la carga y modificación de información mediante formularios
de Django.

---

# Tecnologías

- Django Forms
- ModelForm
- Bootstrap

---

# Formularios implementados

## UsuarioForm

Permite:

- Registrar usuarios.
- Editar usuarios.
- Validar el DNI.

El DNI solamente puede contener números.

Cuando se edita un usuario, el DNI queda bloqueado porque funciona como
clave primaria.

---

## LibroForm

Permite:

- Registrar libros.
- Editar libros.
- Validar el año.
- Seleccionar el estado del libro.

Los libros nuevos comienzan como:

**Disponible**

---

## PrestamoForm

Permite:

- Seleccionar un usuario.
- Seleccionar un libro.

El formulario valida que:

- El libro esté Disponible.
- No exista otro préstamo Activo para ese libro.

---

# Validaciones

Las validaciones se realizan mediante métodos `clean_<campo>()`
y mediante las validaciones propias de los modelos Django.

---

# Estado

Los formularios de usuarios, libros y préstamos están implementados.

## Referencia de documentación consolidada

Para el alcance vigente, contrastar este apunte con `requisitos_funcionales.md`, `requisitos_no_funcionales.md`, `casos_de_uso.md` y `../docs/base_de_datos.md`. La regla actual exige bloquear el cambio manual del estado de un libro con préstamo activo.
