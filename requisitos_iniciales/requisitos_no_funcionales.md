# Requisitos no funcionales — versión consolidada

- RNF-01 — Seguridad: usar autenticación, autorización por rol, CSRF y validación de entradas en servidor.
- RNF-02 — Integridad: impedir préstamos duplicados y proteger el estado del libro durante un préstamo activo.
- RNF-03 — Privacidad: cada lector solo debe acceder a su propio perfil, préstamos, solicitudes y casos de soporte.
- RNF-04 — Mantenibilidad: separar modelos, vistas, formularios, URLs, plantillas y documentación.
- RNF-05 — Usabilidad: mostrar mensajes claros para errores, confirmaciones y estados.
- RNF-06 — Compatibilidad: interfaz utilizable en navegadores modernos y resoluciones habituales.
- RNF-07 — Recuperación: realizar copias de seguridad de la base de datos y definir su restauración en producción.
- RNF-08 — Configuración: secretos y credenciales deben cargarse desde variables de entorno y no almacenarse en el repositorio.
- RNF-09 — Despliegue: usar configuración de producción, HTTPS y servidor compatible con Django; no usar `runserver` en producción.
- RNF-10 — Verificabilidad: disponer de pruebas automatizadas y una lista de pruebas manuales de los flujos críticos.

Estos requisitos son objetivos de calidad y deben comprobarse antes de afirmar que se cumplen.
