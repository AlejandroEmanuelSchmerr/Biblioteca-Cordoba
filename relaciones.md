# Relaciones reales del modelo — 14/10/2026

- `Usuario` 1:N `Prestamo` por `Prestamo.dni`; FK nullable y `SET_NULL`, con campos históricos para preservar comprobantes.
- `Libro` 1:N `Prestamo` por `Prestamo.id_libro`; FK nullable y `SET_NULL`, con título/autor históricos.
- `Usuario` 1:1 `PerfilBiblioteca` por `PerfilBiblioteca.usuario`; `CASCADE`.
- `auth.User` 1:1 `PerfilBiblioteca` por `PerfilBiblioteca.cuenta`; `CASCADE`.
- `Usuario` 1:N `SolicitudPrestamo`; `PROTECT`.
- `Libro` 1:N `SolicitudPrestamo`; `PROTECT`.
- `auth.User` 1:N `MensajeSoporte`; `CASCADE`.
- `Bibliotecario`: entidad independiente, sin FK a las entidades anteriores; la autorización se resuelve mediante sesión `bibliotecario_id` y el decorador `bibliotecario_required`.

No debe dibujarse una relación directa `Bibliotecario`→`Prestamo/Libro/Usuario` en el ERD porque esos campos no existen en el modelo. En arquitectura sí debe conectarse al mecanismo de autenticación/sesión y a las vistas protegidas.
