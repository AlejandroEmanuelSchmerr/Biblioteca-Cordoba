from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Usuario, Libro, Prestamo


CATEGORIAS = [
    ('Programacion', 'Programación'),
    ('Literatura', 'Literatura'),
    ('Historia', 'Historia'),
    ('Ciencias', 'Ciencias'),
    ('Matematica', 'Matemática'),
    ('Informatica', 'Informática'),
    ('Arte', 'Arte'),
    ('Filosofia', 'Filosofía'),
    ('Derecho', 'Derecho'),
    ('Economia', 'Economía'),
    ('Otros', 'Otros'),
]

EDITORIALES = [
    ('Penguin Random House', 'Penguin Random House'),
    ('Planeta', 'Planeta'),
    ('Santillana', 'Santillana'),
    ('Alfaguara', 'Alfaguara'),
    ('Anagrama', 'Anagrama'),
    ('Salamandra', 'Salamandra'),
    ('Sudamericana', 'Sudamericana'),
    ('Prentice Hall', 'Prentice Hall'),
    ('No Starch Press', 'No Starch Press'),
    ('Otra', 'Otra'),
]


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['dni', 'nombre', 'apellido', 'telefono', 'email']
        labels = {
            'dni': 'DNI',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'telefono': 'Teléfono',
            'email': 'Email',
        }
        widgets = {
            'dni': forms.TextInput(attrs={
                'placeholder': 'Ej: 40123456',
                'inputmode': 'numeric',
                'maxlength': '8',
                'pattern': r'\d{8}',
            }),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Alejandro', 'maxlength': '50', 'autocomplete': 'given-name'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ej: Córdoba', 'maxlength': '50', 'autocomplete': 'family-name'}),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ej: 3511234567',
                'inputmode': 'numeric',
                'maxlength': '12',
                'pattern': r'\d{1,12}',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ej: correo@gmail.com',
                'maxlength': '50',
                'autocomplete': 'email',
                'inputmode': 'email',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['dni'].disabled = True
            self.fields['dni'].help_text = 'El DNI no se puede modificar por ser clave primaria.'

    def clean_dni(self):
        dni = (self.cleaned_data.get('dni') or '').strip()
        if not dni.isdigit():
            raise forms.ValidationError('El DNI debe contener solo números')
        if len(dni) != 8:
            raise forms.ValidationError('El DNI debe contener exactamente 8 números.')
        return dni

    def clean_telefono(self):
        telefono = (self.cleaned_data.get('telefono') or '').strip()
        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono debe contener solo números.')
        if len(telefono) > 12:
            raise forms.ValidationError('El teléfono no puede superar los 12 dígitos.')
        return telefono

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if len(email) > 50:
            raise forms.ValidationError('El correo no puede superar los 50 caracteres.')
        return email


class LibroForm(forms.ModelForm):
    anio_calendario = forms.DateField(
        required=False,
        label='Calendario',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control',
            },
        ),
    )
    editorial_otra = forms.CharField(
        required=False,
        label='Otra editorial',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Escribí la editorial', 'maxlength': '100'}),
    )
    categoria_otra = forms.CharField(
        required=False,
        label='Otra categoría',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Escribí la categoría', 'maxlength': '100'}),
    )

    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'editorial', 'anio', 'categoria', 'estado', 'portada']
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'editorial': 'Editorial',
            'anio': 'Año',
            'categoria': 'Categoría',
            'estado': 'Estado',
            'portada': 'Foto de portada',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ej: Clean Code', 'maxlength': '150'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Ej: Robert C. Martin', 'maxlength': '100'}),
            'editorial': forms.Select(choices=EDITORIALES),
            'anio': forms.NumberInput(attrs={
                'placeholder': 'Ej: 2008',
                'min': '1000',
                'max': '2100',
                'inputmode': 'numeric',
            }),
            'categoria': forms.Select(choices=CATEGORIAS),
            'estado': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Max dinámico para no quedar obsoleto
        self.fields['anio_calendario'].widget.attrs['max'] = timezone.localdate().isoformat()
        self.fields['anio_calendario'].help_text = ''

        if self.instance and self.instance.pk:
            libro_con_prestamo_activo = self.instance.prestamos.filter(estado='Activo').exists()
            if libro_con_prestamo_activo:
                self.fields['estado'].disabled = True
                self.fields['estado'].initial = 'Prestado'
                self.fields['estado'].help_text = (
                    'No se puede cambiar el estado mientras exista un préstamo activo. '
                    'Registrá primero la devolución.'
                )
            if self.instance.editorial not in dict(EDITORIALES):
                self.initial['editorial_otra'] = self.instance.editorial
                self.initial['editorial'] = 'Otra'
            if self.instance.categoria not in dict(CATEGORIAS):
                self.initial['categoria_otra'] = self.instance.categoria
                self.initial['categoria'] = 'Otros'

            self.fields['anio_calendario'].initial = f'{self.instance.anio:04d}-01-01'
        else:
            # Nuevo libro siempre disponible
            self.instance.estado = 'Disponible'
            self.fields['estado'].disabled = True
            self.fields['estado'].initial = 'Disponible'

        self.order_fields([
            'titulo', 'autor', 'editorial', 'editorial_otra',
            'anio', 'anio_calendario', 'categoria', 'categoria_otra',
            'estado', 'portada',
        ])

    def clean_portada(self):
        imagen = self.cleaned_data.get('portada')
        if imagen:
            if imagen.size > 5 * 1024 * 1024:
                raise forms.ValidationError('La imagen no puede superar los 5 MB.')
            try:
                from PIL import Image
                imagen.seek(0)
                with Image.open(imagen) as comprobacion:
                    if comprobacion.format not in ('JPEG', 'PNG', 'WEBP'):
                        raise forms.ValidationError('Formato de imagen no permitido. Usá JPG, PNG o WEBP.')
                    comprobacion.verify()
                imagen.seek(0)
            except forms.ValidationError:
                raise
            except Exception:
                raise forms.ValidationError('El archivo no parece ser una imagen válida.')
        return imagen

    def clean(self):
        cleaned_data = super().clean()
        anio = cleaned_data.get('anio')
        fecha = cleaned_data.get('anio_calendario')
        anio_actual = timezone.localdate().year

        if self.instance and self.instance.pk and self.instance.prestamos.filter(estado='Activo').exists():
            cleaned_data['estado'] = 'Prestado'
            self.instance.estado = 'Prestado'

        if fecha:
            anio = fecha.year
            cleaned_data['anio'] = anio
            self.instance.anio = anio

        if anio is None:
            raise forms.ValidationError('Debés indicar el año del libro.')

        if anio < 1000:
            self.add_error('anio', 'El año debe ser igual o posterior a 1000.')
        elif anio > anio_actual:
            self.add_error('anio', 'El año no puede ser mayor al actual')

        if cleaned_data.get('editorial') == 'Otra':
            otra = (cleaned_data.get('editorial_otra') or '').strip()
            if not otra:
                self.add_error('editorial_otra', 'Escribí el nombre de la editorial.')
            else:
                cleaned_data['editorial'] = otra

        if cleaned_data.get('categoria') == 'Otros':
            otra = (cleaned_data.get('categoria_otra') or '').strip()
            if not otra:
                self.add_error('categoria_otra', 'Escribí el nombre de la categoría.')
            else:
                cleaned_data['categoria'] = otra

        return cleaned_data

    def save(self, commit=True):
        libro = super().save(commit=False)
        libro.editorial = self.cleaned_data.get('editorial', libro.editorial)
        libro.categoria = self.cleaned_data.get('categoria', libro.categoria)
        if commit:
            libro.save()
        return libro


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['dni', 'id_libro']
        labels = {
            'dni': 'Usuario',
            'id_libro': 'Libro',
        }
        widgets = {
            'dni': forms.Select(attrs={'class': 'form-select'}),
            'id_libro': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dni'].queryset = Usuario.objects.all().order_by('apellido', 'nombre')
        self.fields['id_libro'].queryset = Libro.objects.all().order_by('titulo')
        self.fields['dni'].empty_label = 'Seleccionar usuario ▼'
        self.fields['id_libro'].empty_label = 'Seleccionar libro ▼'

    def clean_id_libro(self):
        libro = self.cleaned_data.get('id_libro')
        if not libro:
            return libro

        if self.instance and self.instance.pk:
            return libro

        if libro.estado != 'Disponible':
            raise forms.ValidationError(
                f"❌ El libro '{libro.titulo}' está en estado {libro.estado}. No se puede prestar."
            )

        if Prestamo.objects.filter(id_libro=libro, estado='Activo').exists():
            raise forms.ValidationError(
                f"❌ El libro '{libro.titulo}' ya tiene un préstamo activo. Debe devolverlo primero."
            )

        return libro


class RegistroBibliotecaForm(forms.Form):
    dni = forms.CharField(
        max_length=8,
        label='DNI',
        widget=forms.TextInput(attrs={
            'maxlength': '8',
            'inputmode': 'numeric',
            'pattern': '[0-9]{8}',
            'autocomplete': 'off',
        }),
    )
    nombre = forms.CharField(max_length=50, label='Nombre', widget=forms.TextInput(attrs={'maxlength': '50', 'autocomplete': 'given-name'}))
    apellido = forms.CharField(max_length=50, label='Apellido', widget=forms.TextInput(attrs={'maxlength': '50', 'autocomplete': 'family-name'}))
    telefono = forms.CharField(max_length=12, label='Teléfono', widget=forms.TextInput(attrs={'maxlength': '12', 'inputmode': 'numeric', 'pattern': '[0-9]{1,12}'}))
    email = forms.EmailField(max_length=50, label='Correo electrónico', widget=forms.EmailInput(attrs={'maxlength': '50', 'autocomplete': 'email', 'inputmode': 'email'}))
    password = forms.CharField(min_length=10, max_length=128, label='Contraseña', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password_confirm = forms.CharField(min_length=10, max_length=128, label='Repetir contraseña', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

    def clean_dni(self):
        dni = (self.cleaned_data.get('dni') or '').strip()
        if not dni.isdigit() or len(dni) != 8:
            raise forms.ValidationError('El DNI debe contener exactamente 8 números.')
        if Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError('Ya existe una ficha con ese DNI. Acercate al bibliotecario para vincular tu cuenta de forma segura.')
        return dni

    def clean_telefono(self):
        telefono = (self.cleaned_data.get('telefono') or '').strip()
        if not telefono.isdigit() or len(telefono) > 12:
            raise forms.ValidationError('El teléfono debe contener entre 1 y 12 números.')
        return telefono

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if len(email) > 50:
            raise forms.ValidationError('El correo no puede superar los 50 caracteres.')
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ese correo ya está registrado en la biblioteca.')
        from django.contrib.auth import get_user_model
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ese correo ya está asociado a una cuenta.')
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') and cleaned.get('password_confirm') and cleaned['password'] != cleaned['password_confirm']:
            self.add_error('password_confirm', 'Las contraseñas no coinciden.')
        if cleaned.get('password'):
            from django.contrib.auth.password_validation import validate_password
            from django.contrib.auth import get_user_model
            user = get_user_model()(username=cleaned.get('dni', ''), email=cleaned.get('email', ''))
            try:
                validate_password(cleaned['password'], user=user)
            except ValidationError as exc:
                self.add_error('password', exc)
        return cleaned