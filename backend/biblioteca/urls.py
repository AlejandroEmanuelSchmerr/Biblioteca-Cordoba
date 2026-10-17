from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Panel principal bibliotecario
    path("", views.inicio, name="inicio"),

    # Usuarios
    path("usuarios/nuevo/", views.usuario_crear, name="usuario_nuevo"),
    path("usuarios/", views.usuario_lista, name="usuario_lista"),
    path("usuarios/editar/<str:dni>/", views.usuario_editar, name="usuario_editar"),
    path("usuarios/eliminar/<str:dni>/", views.usuario_eliminar, name="usuario_eliminar"),

    # Libros
    path("libros/nuevo/", views.libro_crear, name="libro_nuevo"),
    path("libros/", views.libro_lista, name="libro_lista"),
    path("libros/editar/<int:id_libro>/", views.libro_editar, name="libro_editar"),
    path("libros/eliminar/<int:id_libro>/", views.libro_eliminar, name="libro_eliminar"),

    # Préstamos (bibliotecario)
    path("prestamos/nuevo/", views.prestamo_crear, name="prestamo_nuevo"),
    path("prestamos/", views.prestamo_lista, name="prestamo_lista"),
    path("prestamos/historial/", views.prestamo_historial, name="prestamo_historial"),
    path("prestamos/<int:id_prestamo>/comprobante.pdf", views.prestamo_comprobante_pdf, name="prestamo_comprobante_pdf"),
    path("prestamos/devolver/<int:id_prestamo>/", views.prestamo_devolver, name="prestamo_devolver"),

    # Autenticación
    path("login/", views.iniciar_sesion, name="login"),
    path("bibliotecario/login/", views.iniciar_sesion_bibliotecario, name="bibliotecario_login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("registro/", views.registro_usuario, name="registro_usuario"),
    path("activar/<uidb64>/<token>/", views.activar_cuenta, name="activar_cuenta"),

    # Recuperación contraseña
    path(
        "recuperar-contrasena/",
        auth_views.PasswordResetView.as_view(
            template_name="biblioteca/password_reset_form.html",
            email_template_name="biblioteca/password_reset_email.txt",
            subject_template_name="biblioteca/password_reset_subject.txt",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "recuperar-contrasena/enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="biblioteca/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "restablecer-contrasena/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="biblioteca/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "restablecer-contrasena/completado/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="biblioteca/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    # Portal lector
    path("mi-cuenta/", views.portal_usuario, name="portal_usuario"),
    path("mi-cuenta/solicitar/<int:id_libro>/", views.solicitar_libro, name="solicitar_libro"),
    path("mi-cuenta/prestamos/<int:id_prestamo>/comprobante.pdf", views.comprobante_usuario_pdf, name="comprobante_usuario_pdf"),
    path("mi-cuenta/chat/", views.chat_usuario, name="chat_usuario"),
    path("mi-cuenta/soporte/<int:id_mensaje>/cerrar/", views.cerrar_caso_soporte_usuario, name="cerrar_caso_soporte_usuario"),

    # Panel bibliotecario - solicitudes y soporte
    path("bibliotecario/solicitudes/", views.solicitudes_bibliotecario, name="solicitudes_bibliotecario"),
    path("bibliotecario/solicitudes/<int:id_solicitud>/", views.responder_solicitud, name="responder_solicitud"),
    path("bibliotecario/soporte/", views.bandeja_soporte, name="bandeja_soporte"),
    path("bibliotecario/soporte/<int:id_mensaje>/", views.responder_soporte, name="responder_soporte"),
    path("bibliotecario/soporte/<int:id_mensaje>/cerrar/", views.cerrar_caso_soporte_bibliotecario, name="cerrar_caso_soporte_bibliotecario"),

    # Legales
    path("privacidad/", views.pagina_legal, {"tipo": "privacidad"}, name="politica_privacidad"),
    path("terminos/", views.pagina_legal, {"tipo": "terminos"}, name="terminos_condiciones"),
    path("cookies/", views.pagina_legal, {"tipo": "cookies"}, name="politica_cookies"),
    path("reembolsos/", views.pagina_legal, {"tipo": "reembolsos"}, name="politica_reembolsos"),
]