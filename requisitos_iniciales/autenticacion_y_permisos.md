# Autenticación y permisos

- **Lector:** usa cuenta de Django vinculada a una ficha `Usuario` por `PerfilBiblioteca`. Debe consultar únicamente su propia información.
- **Bibliotecario:** usa el modelo independiente `Bibliotecario` y el acceso de bibliotecario implementado en la aplicación.
- **Superusuario:** usa las credenciales del sistema de autenticación de Django para `/admin/`.

No son identidades intercambiables. La protección debe aplicarse en las vistas del servidor, no solo ocultando enlaces en la interfaz. Probar acceso cruzado entre roles y a recursos de otro lector. Consultar `diagramas/arquitectura_roles_y_rutas.mmd` y `docs/roles_y_aislamiento_de_cuentas.md`.
