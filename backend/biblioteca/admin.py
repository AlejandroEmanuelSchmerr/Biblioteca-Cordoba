from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import (
    Usuario,
    Libro,
    Prestamo,
    PerfilBiblioteca,
    SolicitudPrestamo,
    MensajeSoporte,
    Bibliotecario,
)


class BibliotecaAdminSite(AdminSite):
    site_header = "Biblioteca Córdoba · Administración"
    site_title = "Biblioteca Córdoba"
    index_title = "Panel de control"
    site_url = "/"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(
            {
                "total_usuarios": Usuario.objects.count(),
                "total_libros": Libro.objects.count(),
                "libros_disponibles": Libro.objects.filter(estado="Disponible").count(),
                "prestamos_activos": Prestamo.objects.filter(estado="Activo").count(),
                "solicitudes_pendientes": SolicitudPrestamo.objects.filter(estado="Pendiente").count(),
                "mensajes_pendientes": MensajeSoporte.objects.filter(atendido=False).count(),
                "bibliotecarios_activos": Bibliotecario.objects.filter(activo=True).count(),
            }
        )
        return super().index(request, extra_context=extra_context)

    def has_permission(self, request):
        return bool(request.user and request.user.is_active and request.user.is_superuser)


# Site custom - IMPORTANTE: en config/urls.py usá admin_site.urls, no admin.site.urls
admin_site = BibliotecaAdminSite(name="biblioteca_admin")

# Mantener compatibilidad si otro lado importa admin.site
admin.site = admin_site
admin.sites.site = admin_site


@admin.register(Usuario, site=admin_site)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("dni", "nombre", "apellido", "email", "telefono")
    list_display_links = ("dni", "nombre")
    search_fields = ("dni", "nombre", "apellido", "email")
    ordering = ("apellido", "nombre")
    list_per_page = 25
    fieldsets = (
        ("Identificación", {"fields": ("dni",)}),
        ("Datos personales", {"fields": (("nombre", "apellido"), ("telefono", "email"))}),
    )


@admin.register(Libro, site=admin_site)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("id_libro", "titulo", "autor", "categoria", "estado", "anio")
    list_display_links = ("id_libro", "titulo")
    list_filter = ("estado", "categoria", "anio")
    search_fields = ("titulo", "autor", "editorial", "categoria")
    ordering = ("titulo",)
    list_per_page = 25
    fieldsets = (
        (
            "Información del libro",
            {"fields": (("titulo", "autor"), ("editorial", "anio"), ("categoria", "portada"))},
        ),
        (
            "Disponibilidad",
            {
                "fields": ("estado",),
                "description": "Los libros con préstamos activos deben conservar el estado Prestado.",
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj and obj.prestamos.filter(estado="Activo").exists():
            if "estado" not in readonly:
                readonly.append("estado")
        return tuple(readonly)

    def save_model(self, request, obj, form, change):
        # Si tiene préstamo activo, forzar estado Prestado
        if obj.pk and obj.prestamos.filter(estado="Activo").exists():
            obj.estado = "Prestado"
        super().save_model(request, obj, form, change)


@admin.register(Prestamo, site=admin_site)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "id_prestamo",
        "usuario_mostrado",
        "libro_mostrado",
        "bibliotecario_registra",
        "fecha_prestamo",
        "fecha_devolucion",
        "estado",
    )
    list_filter = ("estado", "fecha_prestamo", "fecha_devolucion")
    search_fields = (
        "usuario_nombre_historico",
        "usuario_dni_historico",
        "libro_titulo_historico",
        "libro_autor_historico",
    )
    list_select_related = ("dni", "id_libro", "bibliotecario_registra")
    list_per_page = 25
    readonly_fields = (
        "fecha_prestamo",
        "usuario_nombre_historico",
        "usuario_dni_historico",
        "libro_titulo_historico",
        "libro_autor_historico",
    )

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Lector")
    def usuario_mostrado(self, obj):
        return obj.usuario_mostrado

    @admin.display(description="Libro")
    def libro_mostrado(self, obj):
        return obj.libro_mostrado


@admin.register(PerfilBiblioteca, site=admin_site)
class PerfilBibliotecaAdmin(admin.ModelAdmin):
    list_display = ("cuenta", "usuario", "creado")
    search_fields = ("cuenta__username", "usuario__dni", "usuario__email", "usuario__nombre", "usuario__apellido")
    list_select_related = ("cuenta", "usuario")
    readonly_fields = ("creado",)


@admin.register(SolicitudPrestamo, site=admin_site)
class SolicitudPrestamoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "libro", "estado", "bibliotecario_responsable", "creada", "respondida")
    list_filter = ("estado", "creada")
    search_fields = ("usuario__dni", "usuario__nombre", "usuario__apellido", "libro__titulo")
    list_select_related = ("usuario", "libro", "bibliotecario_responsable")
    readonly_fields = ("creada",)
    list_per_page = 25


@admin.register(MensajeSoporte, site=admin_site)
class MensajeSoporteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario_cuenta",
        "solicita_persona",
        "bibliotecario_responde",
        "atendido",
        "creado",
        "respondido",
    )
    list_filter = ("solicita_persona", "atendido", "creado")
    search_fields = ("usuario_cuenta__username", "mensaje", "respuesta")
    list_select_related = ("usuario_cuenta", "bibliotecario_responde")
    readonly_fields = ("creado", "respondido")
    list_per_page = 25


class BibliotecarioAdminForm(forms.ModelForm):
    nueva_contrasena = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        required=False,
        help_text="Obligatoria al crear. Al editar, dejala vacía para conservar la contraseña actual.",
    )

    class Meta:
        model = Bibliotecario
        fields = ("username", "nombre", "apellido", "email", "activo", "nueva_contrasena")

    def clean(self):
        cleaned = super().clean()
        if not self.instance.pk and not cleaned.get("nueva_contrasena"):
            self.add_error("nueva_contrasena", "La contraseña es obligatoria al crear un bibliotecario.")
        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        password = self.cleaned_data.get("nueva_contrasena")
        if password:
            obj.set_password(password)
        if commit:
            obj.save()
        return obj


@admin.register(Bibliotecario, site=admin_site)
class BibliotecarioAdmin(admin.ModelAdmin):
    form = BibliotecarioAdminForm
    list_display = ("username", "nombre", "apellido", "email", "activo", "creado")
    list_filter = ("activo", "creado")
    search_fields = ("username", "nombre", "apellido", "email")
    readonly_fields = ("creado",)
    list_per_page = 25
    fieldsets = (
        (
            "Cuenta del bibliotecario",
            {"fields": (("username", "activo"), ("nombre", "apellido"), "email", "nueva_contrasena")},
        ),
    )