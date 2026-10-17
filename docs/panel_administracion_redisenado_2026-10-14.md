# Panel de administración Django — 14/10/2026

Se personalizó el admin estándar de Django para Biblioteca Córdoba con identidad visual verde, acentos dorados, encabezado propio, tarjetas, tablas legibles, filtros, búsquedas y formularios agrupados. El panel `/admin/` continúa reservado a cuentas Django activas con `is_superuser=True`; el bibliotecario usa su acceso separado.

## Archivos
- `backend/biblioteca/admin.py`: listados, filtros, búsquedas, orden, formularios y protección de historial.
- `backend/templates/admin/base_site.html`: marca del panel.
- `backend/templates/admin/index.html`: bienvenida del panel.
- `backend/biblioteca/static/biblioteca/admin-biblioteca.css`: estilos visuales.

## Prueba
Desde `backend`: `python manage.py check` y `python manage.py runserver`; entrar a `/admin/` con una cuenta superusuario. En producción ejecutar `collectstatic`.

Nota: es una mejora visual del admin nativo, no un cambio de autenticación ni una promesa de seguridad completa. Revisar que `PrestamoAdmin` impide borrar historial, y que el estado de libros con préstamos activos se valida también en la lógica de negocio.
