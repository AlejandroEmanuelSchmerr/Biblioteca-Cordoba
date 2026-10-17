# Árbitro de calidad anti-slop — 20 reglas manuales

Este archivo es una lista de revisión local; no afirma que se haya instalado ni ejecutado un arbitro externo de GitHub, Thermos o Skillspector. Verificar los repositorios/herramientas concretos antes de instalar herramientas de terceros.

1. No inventar funciones que no existan.
2. No afirmar que tests pasaron sin ejecutarlos.
3. No afirmar seguridad absoluta o “cero vulnerabilidades”.
4. Validar entradas en formularios y servidor.
5. Limitar longitudes de todos los campos.
6. Usar CSRF en formularios POST.
7. Verificar permisos en cada vista, no solo ocultar enlaces.
8. No exponer datos de otros lectores.
9. Usar ORM parametrizado; evitar SQL concatenado.
10. No registrar secretos ni contraseñas.
11. No subir `.env` al repositorio.
12. No enviar datos personales innecesarios a la IA.
13. Marcar claramente respuestas generadas por IA.
14. No inventar políticas, direcciones, horarios o disponibilidad.
15. Mantener estados de soporte hasta cierre explícito.
16. Evitar duplicar tickets por doble clic.
17. Conservar historial sin mezclar autores.
18. Comprobar enlaces, rutas y estados vacíos.
19. Revisar accesibilidad, contraste y teclado.
20. Actualizar documentación, migraciones, diagramas y pruebas con cada cambio.
