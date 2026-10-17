# Inventario de límites y validaciones — 14/10/2026

Este documento refleja límites declarados en modelos y formularios inspeccionados. HTML `maxlength` es solo una ayuda; la validación del servidor es la autoridad. Los límites de archivos se verifican en formularios y deben probarse con solicitudes manipuladas.

| Modelo/campo | Límite o regla |
|---|---|
| Usuario.dni | 8 caracteres, exactamente 8 dígitos |
| Usuario.nombre / apellido | 50 caracteres cada uno |
| Usuario.telefono | hasta 12 dígitos |
| Usuario.email | máximo 50 caracteres y formato email |
| Libro.titulo | 150 caracteres |
| Libro.autor / editorial / categoria | 100 caracteres cada uno |
| Libro.anio | entero; formulario entre 1000 y año actual |
| Libro.estado | choices Disponible/Prestado/Reservado; préstamo activo fuerza Prestado |
| Libro.portada | JPG/JPEG/PNG/WEBP, máximo 5 MB en formulario |
| Prestamo.usuario_nombre_historico | 110 caracteres |
| Prestamo.usuario_dni_historico | 8 caracteres |
| Prestamo.libro_titulo_historico | 150 caracteres |
| Prestamo.libro_autor_historico | 100 caracteres |
| PerfilBiblioteca.creado | fecha/hora automática |
| SolicitudPrestamo.estado | choices Pendiente/Aprobada/Rechazada, campo max 12 |
| SolicitudPrestamo.nota_bibliotecario | 300 caracteres |
| MensajeSoporte.mensaje | 1500 caracteres |
| MensajeSoporte.respuesta | 3000 caracteres |
| Bibliotecario.username | máximo 60, único |
| Bibliotecario.nombre / apellido | máximo 80 cada uno |
| Bibliotecario.email | máximo 50, único |
| Bibliotecario.password | hash con almacenamiento máximo 128 |
| RegistroBibliotecaForm.password | entre 10 y 128 caracteres |
| Editorial/categoría alternativa | máximo 100 caracteres |

## Pendientes de despliegue
1. Verificar todas las longitudes en `forms.py` y plantillas de formularios (los campos extra no siempre son columnas de base de datos).
2. Revisar correos existentes antes de migrar a 50 caracteres.
3. Validar tamaño y contenido real de imágenes.
4. Ejecutar `python manage.py check`, `python manage.py makemigrations --check --dry-run` y `python manage.py test`.
