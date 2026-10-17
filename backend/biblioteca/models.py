from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models


def validar_email_biblioteca(value):
    email = (value or '').strip()
    if len(email) > 50:
        raise ValidationError('El correo no puede superar los 50 caracteres.')


class Usuario(models.Model):
    dni = models.CharField(
        max_length=8,
        primary_key=True,
        validators=[RegexValidator(r'^\d{8}$', 'El DNI debe contener exactamente 8 números.')],
    )
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(
        max_length=12,
        validators=[RegexValidator(r'^\d{1,12}$', 'El teléfono debe contener entre 1 y 12 números.')],
    )
    email = models.EmailField(max_length=50, validators=[validar_email_biblioteca])

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.dni}'


class Libro(models.Model):
    ESTADOS = [
        ('Disponible', 'Disponible'),
        ('Prestado', 'Prestado'),
        ('Reservado', 'Reservado'),
    ]

    id_libro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=100)
    editorial = models.CharField(max_length=100)
    anio = models.PositiveIntegerField()
    categoria = models.CharField(max_length=100)
    portada = models.ImageField(
        upload_to='portadas_libros/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        help_text='Imagen JPG, PNG o WEBP. Máximo 5 MB (validado también en el formulario).',
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Disponible')

    class Meta:
        ordering = ['titulo']
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def clean(self):
        if self.pk and self.prestamos.filter(estado='Activo').exists() and self.estado != 'Prestado':
            raise ValidationError(
                {'estado': 'El libro tiene un préstamo activo. Registrá la devolución antes de cambiar su estado.'}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.titulo} - {self.autor}'


class Prestamo(models.Model):
    ESTADOS = [
        ('Activo', 'Activo'),
        ('Devuelto', 'Devuelto'),
    ]

    id_prestamo = models.AutoField(primary_key=True)

    dni = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='prestamos',
    )

    id_libro = models.ForeignKey(
        Libro,
        on_delete=models.SET_NULL,
        null=True,
        related_name='prestamos',
    )

    # Copias históricas
    usuario_nombre_historico = models.CharField(max_length=110, blank=True, default='')
    usuario_dni_historico = models.CharField(max_length=8, blank=True, default='')
    libro_titulo_historico = models.CharField(max_length=150, blank=True, default='')
    libro_autor_historico = models.CharField(max_length=100, blank=True, default='')

    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)

    estado = models.CharField(max_length=20, choices=ESTADOS, default='Activo')

    bibliotecario_registra = models.ForeignKey(
        'Bibliotecario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prestamos_registrados',
        help_text='Personal que registró el préstamo; vacío en registros históricos o automáticos.',
    )

    class Meta:
        ordering = ['-fecha_prestamo', '-id_prestamo']
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'

    def clean(self):
        if not self.pk:
            if not self.id_libro_id:
                return

            if self.id_libro and self.id_libro.estado == 'Prestado':
                raise ValidationError(f"❌ El libro '{self.id_libro.titulo}' ya figura como Prestado.")

            if Prestamo.objects.filter(id_libro=self.id_libro, estado='Activo').exists():
                raise ValidationError(
                    f"❌ Ya existe un préstamo activo para el libro '{self.id_libro.titulo}'. Debe devolverlo antes."
                )

    def save(self, *args, **kwargs):
        if self.dni_id and not self.usuario_nombre_historico:
            self.usuario_nombre_historico = f'{self.dni.nombre} {self.dni.apellido}'
            self.usuario_dni_historico = self.dni.dni

        if self.id_libro_id and not self.libro_titulo_historico:
            self.libro_titulo_historico = self.id_libro.titulo
            self.libro_autor_historico = self.id_libro.autor

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def usuario_mostrado(self):
        if self.dni_id:
            return f'{self.dni.nombre} {self.dni.apellido}'
        return self.usuario_nombre_historico or 'Usuario eliminado'

    @property
    def libro_mostrado(self):
        if self.id_libro_id:
            return self.id_libro.titulo
        return self.libro_titulo_historico or 'Libro eliminado'

    def __str__(self):
        return f'Prestamo {self.id_prestamo}: {self.usuario_mostrado} - {self.libro_mostrado} ({self.estado})'


class PerfilBiblioteca(models.Model):
    """Vincula una cuenta autenticada con su ficha de biblioteca."""
    cuenta = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil_biblioteca'
    )
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_cuenta')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil de biblioteca'
        verbose_name_plural = 'Perfiles de biblioteca'

    def __str__(self):
        return f'Cuenta de {self.usuario}'


class SolicitudPrestamo(models.Model):
    ESTADOS = [('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada')]

    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='solicitudes_prestamo')
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name='solicitudes_prestamo')
    estado = models.CharField(max_length=12, choices=ESTADOS, default='Pendiente')
    creada = models.DateTimeField(auto_now_add=True)
    respondida = models.DateTimeField(null=True, blank=True)
    nota_bibliotecario = models.CharField(max_length=300, blank=True, default='')
    bibliotecario_responsable = models.ForeignKey(
        'Bibliotecario', on_delete=models.SET_NULL, null=True, blank=True, related_name='solicitudes_atendidas'
    )

    class Meta:
        ordering = ['-creada']
        verbose_name = 'Solicitud de préstamo'
        verbose_name_plural = 'Solicitudes de préstamo'

    def __str__(self):
        return f'{self.usuario} - {self.libro} ({self.estado})'


class MensajeSoporte(models.Model):
    usuario_cuenta = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_biblioteca'
    )
    mensaje = models.CharField(max_length=1500)
    respuesta = models.CharField(max_length=3000, blank=True, default='')
    solicita_persona = models.BooleanField(default=False)
    atendido = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    respondido = models.DateTimeField(null=True, blank=True)
    bibliotecario_responde = models.ForeignKey(
        'Bibliotecario', on_delete=models.SET_NULL, null=True, blank=True, related_name='mensajes_respondidos'
    )

    class Meta:
        ordering = ['creado']
        verbose_name = 'Mensaje de soporte'
        verbose_name_plural = 'Mensajes de soporte'

    def __str__(self):
        return f'Mensaje #{self.pk} de {self.usuario_cuenta.username}'


class Bibliotecario(models.Model):
    """Identidad y credenciales del personal, separadas de auth.User y Usuario lector."""
    username = models.CharField(max_length=60, unique=True)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['username']
        verbose_name = 'Bibliotecario'
        verbose_name_plural = 'Bibliotecarios'

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.username})'