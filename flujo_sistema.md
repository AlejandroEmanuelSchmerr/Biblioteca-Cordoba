# Flujo general del sistema

```mermaid
flowchart TD
    A[Inicio] --> B{Tipo de acceso}
    B -->|Lector| C[Registro o inicio de sesión]
    C --> D[Portal del lector]
    D --> E[Catálogo y solicitudes]
    D --> F[Préstamos, comprobantes y soporte propios]
    B -->|Bibliotecario| G[Inicio de sesión de bibliotecario]
    G --> H[Panel de gestión]
    H --> I[Usuarios y libros]
    H --> J[Solicitudes y soporte]
    H --> K[Préstamos y devoluciones]
    B -->|Superusuario| L[Panel Django Admin]
```

El detalle del ciclo de préstamo y devolución está en `diagramas/Diagrama_Flujo_Prestamo.drawio`.


> Revisión de paquete: 14/10/2026. Ver también `docs/diagramas_y_modelos_2026-10-14.md` y `docs/limite_email_50_2026-10-14.md` para los diagramas editables y el límite actualizado de correo.
