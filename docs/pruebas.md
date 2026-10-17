# Plan de pruebas

## Comandos automatizados

Ejecutar desde `backend/` con el entorno virtual activado:

```powershell
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```

Estos comandos deben ejecutarse en la máquina de desarrollo o CI con las dependencias instaladas. No marcar como aprobados resultados que todavía no se hayan ejecutado.

## Casos manuales mínimos

| Área | Prueba | Resultado esperado |
|---|---|---|
| Acceso | Abrir una ruta privada sin iniciar sesión | Redirección o denegación de acceso |
| Roles | Intentar abrir una ruta de bibliotecario con cuenta de lector | Acceso denegado |
| Libros | Crear/editar libro con datos inválidos | Mensaje de validación y no guardar datos inválidos |
| Préstamo | Prestar un libro disponible | Préstamo activo y libro `Prestado` |
| Duplicado | Intentar prestar un libro ya prestado | Operación rechazada |
| Estado | Intentar cambiar manualmente un libro con préstamo activo | Operación bloqueada en interfaz y servidor |
| Devolución | Devolver un préstamo activo | Estado `Devuelto`, fecha registrada y libro disponible |
| Historial | Consultar un préstamo devuelto | Registro y datos históricos conservados |
| Solicitudes | Enviar y responder una solicitud | Estado y nota visibles para el lector correspondiente |
| Soporte | Crear caso, responder y cerrar | Historial correcto y estado coherente |
| BiblioBot | Consultar una pregunta conocida y una desconocida | Respuesta pertinente o indicación clara de límites |
| Seguridad | Enviar POST sin CSRF / sin permisos | Petición rechazada según configuración |

## Registro de resultados

Anotar fecha, versión/commit, entorno, comando o paso ejecutado y resultado. Este documento es un plan de pruebas; no representa evidencia de que todos los casos ya hayan pasado.
