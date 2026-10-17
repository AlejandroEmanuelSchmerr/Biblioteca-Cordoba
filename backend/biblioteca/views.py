from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from django.db.models.deletion import ProtectedError
from .forms import UsuarioForm, LibroForm, PrestamoForm, RegistroBibliotecaForm
from .models import Usuario, Libro, Prestamo, PerfilBiblioteca, SolicitudPrestamo, MensajeSoporte, Bibliotecario
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.core import signing
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
import json, os, urllib.request, urllib.error
from functools import wraps
from django.contrib.auth.hashers import check_password

def bibliotecario_required(view_func):
    """Autoriza únicamente una sesión vinculada a la tabla Bibliotecario independiente."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        bid = request.session.get('bibliotecario_id')
        if not bid:
            return redirect('bibliotecario_login')
        try:
            request.bibliotecario = Bibliotecario.objects.get(pk=bid, activo=True)
        except Bibliotecario.DoesNotExist:
            request.session.pop('bibliotecario_id', None)
            return redirect('bibliotecario_login')
        if request.user.is_authenticated:
            # Evita que una sesión de lector y una sesión de personal se mezclen.
            logout(request)
            request.session['bibliotecario_id'] = bid
            request.bibliotecario = Bibliotecario.objects.get(pk=bid, activo=True)
        return view_func(request, *args, **kwargs)
    return _wrapped

@bibliotecario_required
def inicio(request):
    context = {
        "total_usuarios": Usuario.objects.count(),
        "total_libros": Libro.objects.count(),
        "libros_disponibles": Libro.objects.filter(estado="Disponible").count(),
        "total_libros_disponibles": Libro.objects.filter(estado="Disponible").count(),
        "prestamos_activos": Prestamo.objects.filter(estado="Activo").count(),
        "prestamos_historicos": Prestamo.objects.filter(estado="Devuelto").count(),
        "libros_prestados": Libro.objects.filter(estado="Prestado").count(),
        "libros_reservados": Libro.objects.filter(estado="Reservado").count(),
        "total_prestamos": Prestamo.objects.count(),
    }
    total_libros = context["total_libros"] or 1
    context["porcentaje_disponibles"] = round(context["libros_disponibles"] * 100 / total_libros)
    context["porcentaje_prestados"] = round(context["libros_prestados"] * 100 / total_libros)
    context["porcentaje_reservados"] = round(context["libros_reservados"] * 100 / total_libros)
    return render(request, "biblioteca/inicio.html", context)

# --- USUARIOS ---
@bibliotecario_required
def usuario_crear(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect('usuario_lista')
    else:
        form = UsuarioForm()
    return render(request, 'biblioteca/usuario_form.html', {'form': form})

@bibliotecario_required
def usuario_lista(request):
    query = request.GET.get('q', '')
    usuarios = Usuario.objects.all()
    if query:
        usuarios = usuarios.filter(
            Q(nombre__icontains=query) | 
            Q(apellido__icontains=query) | 
            Q(dni__icontains=query) |
            Q(email__icontains=query)
        )
    usuarios = usuarios.order_by('apellido')
    context = { "usuarios": usuarios, "query": query }
    return render(request, 'biblioteca/usuario_lista.html', context)

@bibliotecario_required
def usuario_editar(request, dni):
    usuario = Usuario.objects.filter(dni=dni).first()
    if usuario is None:
        messages.warning(request, 'No se encontró el usuario solicitado. Actualizá el listado e intentá nuevamente.')
        return redirect('usuario_lista')
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuario_lista')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'biblioteca/usuario_form.html', {'form': form, 'usuario': usuario})


@bibliotecario_required
def usuario_eliminar(request, dni):
    # No propagar DoesNotExist/Http404 con detalles internos: un DNI inexistente vuelve al listado.
    usuario = Usuario.objects.filter(dni=dni).first()
    if usuario is None:
        messages.warning(request, 'No se encontró el usuario solicitado. Puede que ya haya sido eliminado.')
        return redirect('usuario_lista')

    if usuario.prestamos.filter(estado='Activo').exists():
        messages.error(
            request,
            'No se puede eliminar este usuario porque tiene préstamos activos. Primero registrá la devolución.'
        )
        return redirect('usuario_lista')

    if request.method == 'POST':
        try:
            usuario.delete()
            messages.success(request, 'Usuario eliminado correctamente.')
            return redirect('usuario_lista')
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar este usuario porque tiene préstamos activos. Primero registrá la devolución.'
            )
            return redirect('usuario_lista')

    return render(request, 'biblioteca/usuario_confirm_delete.html', {'usuario': usuario})

# --- LIBROS ---
@bibliotecario_required
def libro_crear(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('libro_lista')
    else:
        form = LibroForm()
    return render(request, 'biblioteca/libro_form.html', {'form': form})

@bibliotecario_required
def libro_lista(request):
    query = request.GET.get('q', '')
    estado_filtro = request.GET.get('estado', '')
    libros = Libro.objects.all()
    if query:
        libros = libros.filter(
            Q(titulo__icontains=query) | 
            Q(autor__icontains=query) |
            Q(categoria__icontains=query)
        )
    if estado_filtro:
        libros = libros.filter(estado=estado_filtro)
    libros = libros.order_by("titulo")
    context = {
        "libros": libros,
        "query": query,
        "estado_filtro": estado_filtro,
    }
    return render(request, 'biblioteca/libro_lista.html', context)

@bibliotecario_required
def libro_editar(request, id_libro):
    libro = Libro.objects.filter(id_libro=id_libro).first()
    if libro is None:
        messages.warning(request, 'No se encontró el libro solicitado. Actualizá el catálogo e intentá nuevamente.')
        return redirect('libro_lista')
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('libro_lista')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'biblioteca/libro_form.html', {'form': form, 'libro': libro})

@bibliotecario_required
def libro_eliminar(request, id_libro):
    libro = Libro.objects.filter(id_libro=id_libro).first()
    if libro is None:
        messages.warning(request, 'No se encontró el libro solicitado. Puede que ya haya sido eliminado.')
        return redirect('libro_lista')

    if libro.prestamos.filter(estado='Activo').exists():
        messages.error(
            request,
            'No se puede eliminar este libro porque tiene préstamos activos. Primero registrá la devolución.'
        )
        return redirect('libro_lista')

    if request.method == 'POST':
        try:
            libro.delete()
            messages.success(request, 'Libro eliminado correctamente.')
            return redirect('libro_lista')
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar este libro porque tiene préstamos activos. Primero registrá la devolución.'
            )
            return redirect('libro_lista')

    return render(request, 'biblioteca/libro_confirm_delete.html', {'libro': libro})

# --- PRESTAMOS ---
@bibliotecario_required
def prestamo_crear(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    prestamo = form.save(commit=False)
                    prestamo.estado = "Activo"
                    prestamo.bibliotecario_registra = request.bibliotecario
                    prestamo.save()

                    libro = prestamo.id_libro
                    libro.estado = "Prestado"
                    libro.save()

                    messages.success(request, f"✅ Préstamo registrado: {libro.titulo} -> {prestamo.dni}")
                    return redirect('prestamo_lista')
            except ValidationError as e:
                form.add_error('id_libro', e.messages)
    else:
        form = PrestamoForm()
    return render(request, 'biblioteca/prestamo_form.html', {'form': form})

@bibliotecario_required
def prestamo_lista(request):
    query = request.GET.get('q', '')
    estado_filtro = request.GET.get('estado', '')
    prestamos = Prestamo.objects.select_related('dni', 'id_libro').all()
    
    if query:
        prestamos = prestamos.filter(
            Q(dni__nombre__icontains=query) |
            Q(dni__apellido__icontains=query) |
            Q(dni__dni__icontains=query) |
            Q(id_libro__titulo__icontains=query) |
            Q(id_libro__autor__icontains=query) |
            Q(usuario_nombre_historico__icontains=query) |
            Q(usuario_dni_historico__icontains=query) |
            Q(libro_titulo_historico__icontains=query) |
            Q(libro_autor_historico__icontains=query)
        )
    if estado_filtro:
        prestamos = prestamos.filter(estado=estado_filtro)
        
    prestamos = prestamos.order_by('-fecha_prestamo')
    context = {
        'prestamos': prestamos,
        'query': query,
        'estado_filtro': estado_filtro,
        'hay_activos': Prestamo.objects.filter(estado='Activo').exists(),
        'modo_historial': False,
    }
    return render(request, 'biblioteca/prestamo_lista.html', context)

@bibliotecario_required
def prestamo_devolver(request, id_prestamo):
    if request.method != 'POST':
        messages.error(
            request,
            'La devolución debe realizarse mediante el botón seguro de la tabla de préstamos.'
        )
        return redirect('prestamo_lista')

    prestamo = get_object_or_404(Prestamo, id_prestamo=id_prestamo)

    if prestamo.estado == 'Devuelto':
        messages.warning(request, f'El préstamo {id_prestamo} ya fue devuelto.')
        return redirect('prestamo_lista')

    with transaction.atomic():
        libro = prestamo.id_libro
        # Primero cerrar el préstamo: Libro.clean() bloquea cambios de estado
        # mientras detecte cualquier préstamo Activo asociado.
        prestamo.estado = 'Devuelto'
        prestamo.fecha_devolucion = timezone.localdate()
        prestamo.save()

        if libro is not None:
            libro.estado = 'Disponible'
            libro.save()

    messages.success(
        request,
        f"📚 Libro '{prestamo.libro_mostrado}' devuelto correctamente." if libro is None else f"📚 Libro '{libro.titulo}' devuelto correctamente. Ya está Disponible."
    )

    return redirect('prestamo_lista')

@bibliotecario_required
def prestamo_historial(request):
    query = request.GET.get('q', '')
    prestamos = Prestamo.objects.select_related('dni', 'id_libro').filter(estado='Devuelto')
    if query:
        prestamos = prestamos.filter(
            Q(dni__nombre__icontains=query) | Q(dni__apellido__icontains=query) |
            Q(dni__dni__icontains=query) | Q(id_libro__titulo__icontains=query) |
            Q(usuario_nombre_historico__icontains=query) | Q(usuario_dni_historico__icontains=query) |
            Q(libro_titulo_historico__icontains=query)
        )
    return render(request, 'biblioteca/prestamo_historial.html', {'prestamos': prestamos.order_by('-fecha_prestamo'), 'query': query, 'modo_historial': True})


@bibliotecario_required
def prestamo_comprobante_pdf(request, id_prestamo):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id_prestamo)
    buffer = BytesIO()

    # Diseño de comprobante con bloques, tabla de datos y texto ajustado.
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=22 * mm, leftMargin=22 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
        title=f"Comprobante de préstamo {prestamo.id_prestamo}",
        author="Biblioteca Córdoba",
    )
    azul = colors.HexColor("#1F4E79")
    azul_claro = colors.HexColor("#EAF2F8")
    gris = colors.HexColor("#526174")
    borde = colors.HexColor("#D5DEE8")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="BCBrand", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=21, leading=26, textColor=azul, alignment=TA_CENTER,
        spaceAfter=4 * mm,
    ))
    styles.add(ParagraphStyle(
        name="BCSub", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10, leading=14, textColor=gris, alignment=TA_CENTER,
        spaceAfter=8 * mm,
    ))
    styles.add(ParagraphStyle(
        name="BCLabel", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=9, leading=13, textColor=azul,
    ))
    styles.add(ParagraphStyle(
        name="BCValue", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10, leading=14, textColor=colors.HexColor("#202B38"),
    ))
    styles.add(ParagraphStyle(
        name="BCNote", parent=styles["Normal"], fontName="Helvetica-Oblique",
        fontSize=8, leading=11, textColor=gris, alignment=TA_CENTER,
    ))

    dni = prestamo.dni.dni if prestamo.dni_id else (prestamo.usuario_dni_historico or "No disponible")
    autor = (prestamo.id_libro.autor if prestamo.id_libro_id else prestamo.libro_autor_historico) or "No disponible"
    fecha_devolucion = prestamo.fecha_devolucion.strftime("%d/%m/%Y") if prestamo.fecha_devolucion else "Pendiente"
    datos = [
        ("N.º de comprobante", str(prestamo.id_prestamo)),
        ("Estado", prestamo.get_estado_display()),
        ("Usuario", prestamo.usuario_mostrado or "No disponible"),
        ("DNI", dni),
        ("Libro", prestamo.libro_mostrado or "No disponible"),
        ("Autor", autor),
        ("Fecha del préstamo", prestamo.fecha_prestamo.strftime("%d/%m/%Y")),
        ("Fecha de devolución", fecha_devolucion),
    ]
    tabla_datos = [[Paragraph(etiqueta, styles["BCLabel"]), Paragraph(str(valor), styles["BCValue"])] for etiqueta, valor in datos]
    tabla = Table(tabla_datos, colWidths=[53 * mm, 95 * mm], hAlign="CENTER")
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BACKGROUND", (0, 0), (0, -1), azul_claro),
        ("GRID", (0, 0), (-1, -1), 0.6, borde),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story = [
        Spacer(1, 5 * mm),
        Paragraph("BIBLIOTECA CÓRDOBA", styles["BCBrand"]),
        Paragraph("COMPROBANTE DE PRÉSTAMO", styles["BCSub"]),
        tabla,
        Spacer(1, 10 * mm),
        Paragraph(
            "Este comprobante deja constancia de los datos registrados en el sistema "
            "para el préstamo indicado. Conservá este documento como referencia.",
            styles["BCValue"],
        ),
        Spacer(1, 18 * mm),
        Paragraph("Documento generado por el sistema de gestión de Biblioteca Córdoba.", styles["BCNote"]),
    ]
    doc.build(story)
    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    marca_tiempo = timezone.localtime().strftime("%Y%m%d_%H%M%S_%f")
    response["Content-Disposition"] = f'attachment; filename="comprobante_prestamo_{prestamo.id_prestamo}_{marca_tiempo}.pdf"'
    return response


@never_cache
def iniciar_sesion(request):
    """Acceso exclusivo para lectores; las cuentas de personal usan otra ruta."""
    ip = request.META.get('REMOTE_ADDR', 'unknown')
    cache_key = f'login_reader_attempts:{ip}'
    intentos = cache.get(cache_key, 0)
    bloqueado = intentos >= 8
    if request.method == 'POST':
        if bloqueado:
            messages.error(request, 'Demasiados intentos. Esperá unos minutos y probá nuevamente.')
            return render(request, 'biblioteca/login.html', status=429)
        username = request.POST.get('username', '').strip()[:150]
        password = request.POST.get('password', '')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None and usuario.is_active and not usuario.is_staff and not usuario.is_superuser:
            request.session.pop('bibliotecario_id', None)
            login(request, usuario)
            cache.delete(cache_key)
            messages.success(request, 'Inicio de sesión correcto')
            return redirect('portal_usuario')
        cache.set(cache_key, intentos + 1, 600)
        messages.error(request, 'Usuario o contraseña incorrectos. No se pudo iniciar sesión con esos datos. Si sos bibliotecario, usá su acceso separado.')
    return render(request, 'biblioteca/login.html', status=429 if bloqueado else 200)


@never_cache
def iniciar_sesion_bibliotecario(request):
    """Login separado: valida contra biblioteca.Bibliotecario, nunca auth.User."""
    ip = request.META.get('REMOTE_ADDR', 'unknown')
    cache_key = f'login_librarian_attempts:{ip}'
    intentos = cache.get(cache_key, 0)
    bloqueado = intentos >= 8
    if request.method == 'POST':
        if bloqueado:
            messages.error(request, 'Demasiados intentos. Esperá unos minutos y probá nuevamente.')
            return render(request, 'biblioteca/bibliotecario_login.html', status=429)
        username = request.POST.get('username', '').strip()[:60]
        password = request.POST.get('password', '')
        cuenta = Bibliotecario.objects.filter(username__iexact=username, activo=True).first()
        if cuenta and cuenta.check_password(password):
            # Aislar la sesión del lector antes de crear la sesión de personal.
            logout(request)
            request.session.cycle_key()
            request.session['bibliotecario_id'] = cuenta.pk
            cache.delete(cache_key)
            messages.success(request, 'Acceso de bibliotecario correcto')
            return redirect('inicio')
        cache.set(cache_key, intentos + 1, 600)
        messages.error(request, 'Credenciales incorrectas o cuenta de bibliotecario inactiva.')
    return render(request, 'biblioteca/bibliotecario_login.html', status=429 if bloqueado else 200)

def cerrar_sesion(request):
    era_personal = bool(request.session.get('bibliotecario_id'))
    request.session.pop('bibliotecario_id', None)
    if request.user.is_authenticated:
        logout(request)
    request.session.flush()
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('bibliotecario_login' if era_personal else 'login')

# ================= PORTAL PRIVADO DE LECTORES =================
def activar_cuenta(request, uidb64, token):
    # Tokens oficiales de Django: URL segura y coherente con recuperación de contraseña.
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        cuenta = User.objects.get(pk=user_id, is_staff=False, is_superuser=False)
    except (ValueError, TypeError, OverflowError, User.DoesNotExist):
        cuenta = None
    if cuenta is None or not default_token_generator.check_token(cuenta, token):
        messages.error(request, 'El enlace de activación no es válido o ya venció. Solicitá un nuevo enlace o contactá al bibliotecario.')
        return redirect('registro_usuario')
    if not cuenta.is_active:
        cuenta.is_active = True
        cuenta.save(update_fields=['is_active'])
        messages.success(request, 'Correo confirmado. Ya podés iniciar sesión con tu DNI y contraseña.')
    else:
        messages.info(request, 'La cuenta ya estaba activada. Iniciá sesión para continuar.')
    return redirect('login')


def portal_o_perfil(request):
    try:
        return request.user.perfil_biblioteca
    except (PerfilBiblioteca.DoesNotExist, AttributeError):
        return None


@never_cache
def registro_usuario(request):
    if request.session.get('bibliotecario_id'):
        return redirect('inicio')
    if request.user.is_authenticated:
        return redirect('admin:index' if request.user.is_superuser else 'portal_usuario')
    ip = request.META.get('REMOTE_ADDR', 'unknown')
    key = f'registro_attempts:{ip}'
    if cache.get(key, 0) >= 5 and request.method == 'POST':
        messages.error(request, 'Demasiados intentos. Esperá unos minutos y probá nuevamente.')
        return render(request, 'biblioteca/registro_usuario.html', {'form': RegistroBibliotecaForm()}, status=429)
    form = RegistroBibliotecaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            with transaction.atomic():
                datos = form.cleaned_data
                cuenta = User.objects.create_user(username=datos['dni'], email=datos['email'], password=datos['password'], first_name=datos['nombre'][:30], last_name=datos['apellido'][:150], is_staff=False, is_superuser=False, is_active=False)
                ficha = Usuario.objects.create(dni=datos['dni'], nombre=datos['nombre'], apellido=datos['apellido'], telefono=datos['telefono'], email=datos['email'])
                PerfilBiblioteca.objects.create(cuenta=cuenta, usuario=ficha)
                uidb64 = urlsafe_base64_encode(force_bytes(cuenta.pk))
                token = default_token_generator.make_token(cuenta)
                url_activacion = request.build_absolute_uri(reverse('activar_cuenta', args=[uidb64, token]))
                send_mail('Activá tu cuenta de Biblioteca Córdoba', f'Hola {datos["nombre"]}: para confirmar tu correo y activar la cuenta, abrí este enlace: {url_activacion}\n\nSi no solicitaste esta cuenta, ignorá este mensaje.', None, [cuenta.email], fail_silently=False)
            cache.delete(key)
            messages.success(request, 'Cuenta creada. Revisá el correo indicado para confirmar la dirección y activar el acceso.')
            return redirect('login')
        except Exception:
            import logging
            logging.getLogger(__name__).exception('No se pudo completar el registro o enviar el correo de activación')
            cache.set(key, cache.get(key, 0) + 1, 900)
            messages.error(request, 'No se pudo completar el registro o enviar el correo. Revisá la configuración de correo e intentá nuevamente.')
    return render(request, 'biblioteca/registro_usuario.html', {'form': form})


@login_required
def portal_usuario(request):
    if request.session.get('bibliotecario_id'):
        return redirect('inicio')
    if request.user.is_superuser:
        return redirect('admin:index')
    if request.user.is_staff:
        return redirect('inicio')
    perfil = portal_o_perfil(request)
    if perfil is None:
        logout(request)
        messages.error(request, 'La cuenta no tiene una ficha vinculada. Contactá al bibliotecario.')
        return redirect('login')
    prestamos = Prestamo.objects.filter(dni=perfil.usuario).select_related('id_libro').order_by('-fecha_prestamo')
    solicitudes = SolicitudPrestamo.objects.filter(usuario=perfil.usuario).select_related('libro')
    libros = Libro.objects.filter(estado='Disponible').order_by('titulo')
    ticket_actual = MensajeSoporte.objects.filter(usuario_cuenta=request.user, solicita_persona=True, atendido=False).order_by('-creado').first()
    ticket_abierto = bool(ticket_actual)
    return render(request, 'biblioteca/portal_usuario.html', {'perfil': perfil, 'prestamos': prestamos, 'solicitudes': solicitudes, 'libros': libros, 'total_activos': prestamos.filter(estado='Activo').count(), 'ticket_abierto': ticket_abierto, 'ticket_actual': ticket_actual, 'casos_soporte': MensajeSoporte.objects.filter(usuario_cuenta=request.user, solicita_persona=True).order_by('-creado'), 'chat_messages': list(MensajeSoporte.objects.filter(usuario_cuenta=request.user, solicita_persona=False).order_by('-creado')[:12])[::-1]})


@login_required
@require_POST
def solicitar_libro(request, id_libro):
    if request.session.get('bibliotecario_id'):
        return redirect('inicio')
    if request.user.is_superuser:
        return redirect('admin:index')
    if request.user.is_staff:
        return redirect('inicio')
    perfil = portal_o_perfil(request)
    if perfil is None:
        return redirect('login')
    libro = get_object_or_404(Libro, id_libro=id_libro, estado='Disponible')
    ya_activo = Prestamo.objects.filter(dni=perfil.usuario, id_libro=libro, estado='Activo').exists()
    pendiente = SolicitudPrestamo.objects.filter(usuario=perfil.usuario, libro=libro, estado='Pendiente').exists()
    if ya_activo or pendiente:
        messages.info(request, 'Ya tenés un préstamo activo o una solicitud pendiente para ese libro.')
    else:
        SolicitudPrestamo.objects.create(usuario=perfil.usuario, libro=libro)
        messages.success(request, 'Solicitud enviada. El bibliotecario debe confirmarla antes de retirar el libro.')
    return redirect('portal_usuario')


@bibliotecario_required
def solicitudes_bibliotecario(request):
    solicitudes = SolicitudPrestamo.objects.select_related('usuario', 'libro').all()
    return render(request, 'biblioteca/solicitudes_bibliotecario.html', {'solicitudes': solicitudes})


@bibliotecario_required
@require_POST
def responder_solicitud(request, id_solicitud):
    solicitud = get_object_or_404(SolicitudPrestamo.objects.select_related('usuario','libro'), pk=id_solicitud)
    accion = request.POST.get('accion')
    if solicitud.estado != 'Pendiente':
        messages.warning(request, 'Esta solicitud ya fue procesada.')
        return redirect('solicitudes_bibliotecario')
    if accion == 'aprobar':
        try:
            with transaction.atomic():
                libro = Libro.objects.select_for_update().get(pk=solicitud.libro_id)
                if libro.estado != 'Disponible' or Prestamo.objects.filter(id_libro=libro, estado='Activo').exists():
                    messages.error(request, 'El libro ya no está disponible. La solicitud no se aprobó.')
                    return redirect('solicitudes_bibliotecario')
                Prestamo.objects.create(dni=solicitud.usuario, id_libro=libro, estado='Activo', bibliotecario_registra=request.bibliotecario)
                libro.estado = 'Prestado'; libro.save()
                solicitud.estado = 'Aprobada'; solicitud.respondida = timezone.now(); solicitud.bibliotecario_responsable = request.bibliotecario; solicitud.save()
            messages.success(request, 'Solicitud aprobada y préstamo registrado.')
        except ValidationError:
            messages.error(request, 'No se pudo aprobar la solicitud. Revisá el estado del libro.')
    elif accion == 'rechazar':
        solicitud.estado = 'Rechazada'; solicitud.respondida = timezone.now(); solicitud.bibliotecario_responsable = request.bibliotecario; solicitud.save(update_fields=['estado','respondida','bibliotecario_responsable'])
        messages.success(request, 'Solicitud rechazada.')
    return redirect('solicitudes_bibliotecario')


@login_required
def comprobante_usuario_pdf(request, id_prestamo):
    if request.user.is_superuser:
        return redirect('admin:index')
    if request.user.is_staff:
        return redirect('inicio')
    perfil = portal_o_perfil(request)
    if perfil is None:
        return redirect('login')
    # Importante: filtrar por la ficha de la sesión; nunca confiar solo en el ID enviado por URL.
    prestamo = get_object_or_404(Prestamo, id_prestamo=id_prestamo, dni=perfil.usuario)
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    buffer = BytesIO(); doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=22*mm, leftMargin=22*mm, topMargin=22*mm, bottomMargin=22*mm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='LectorTitulo', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=23, leading=28, textColor=colors.HexColor('#087f8c'), alignment=1, spaceAfter=5*mm))
    styles.add(ParagraphStyle(name='LectorSubtitulo', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, textColor=colors.HexColor('#b45309'), alignment=1, spaceAfter=9*mm))
    styles.add(ParagraphStyle(name='LectorNota', parent=styles['Normal'], fontSize=9, leading=13, textColor=colors.HexColor('#475569'), alignment=1))
    story = [Paragraph('BIBLIOTECA CÓRDOBA · MI CUENTA', styles['LectorTitulo']), Paragraph('CONSTANCIA PERSONAL DEL LECTOR', styles['LectorSubtitulo']), Spacer(1, 5*mm)]
    datos = [['REFERENCIA', str(prestamo.id_prestamo)], ['TITULAR', prestamo.usuario_mostrado], ['DNI', perfil.usuario.dni], ['NOMBRE DEL LIBRO', prestamo.libro_mostrado], ['AUTOR', prestamo.libro_autor_historico or (prestamo.id_libro.autor if prestamo.id_libro_id else '-')], ['ENTREGA', prestamo.fecha_prestamo.strftime('%d/%m/%Y')], ['SITUACIÓN', prestamo.estado], ['DEVOLUCIÓN', prestamo.fecha_devolucion.strftime('%d/%m/%Y') if prestamo.fecha_devolucion else 'Pendiente']]
    tabla = Table(datos, colWidths=[48*mm, 100*mm], rowHeights=[12*mm]*len(datos))
    tabla.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#087f8c')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('BACKGROUND',(0,1),(0,-1),colors.HexColor('#e0f2f1')),('TEXTCOLOR',(0,1),(0,-1),colors.HexColor('#115e59')),('BACKGROUND',(1,1),(1,-1),colors.HexColor('#fffbeb')),('TEXTCOLOR',(1,1),(1,-1),colors.HexColor('#1f2937')),('LINEBELOW',(0,0),(-1,-1),.6,colors.HexColor('#99c8c7')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11)]))
    story.extend([tabla, Spacer(1, 15*mm), Paragraph('Documento personal descargado desde el portal del lector. No reemplaza una constancia firmada por la institución.', styles['LectorNota']), Spacer(1, 8*mm), Paragraph('BIBLIOTECA CÓRDOBA · PROYECTO PERSONAL 2026', styles['LectorNota'])])
    doc.build(story)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf'); marca_tiempo = timezone.localtime().strftime('%Y%m%d_%H%M%S_%f'); response['Content-Disposition'] = f'attachment; filename="comprobante_personal_lector_{prestamo.id_prestamo}_{marca_tiempo}.pdf"'; return response


@login_required
@require_POST
def chat_usuario(request):
    if request.session.get('bibliotecario_id'):
        return redirect('inicio')
    if request.user.is_staff:
        return JsonResponse({'error':'Usá la bandeja de soporte del bibliotecario.'}, status=403)
    perfil = portal_o_perfil(request)
    if perfil is None:
        return JsonResponse({'error':'Cuenta sin ficha vinculada.'}, status=403)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'error':'Mensaje no válido.'}, status=400)
    texto = str(payload.get('message','')).strip()[:1500]
    humano = bool(payload.get('human', False))
    if not texto and not humano:
        return JsonResponse({'error':'Escribí una consulta.'}, status=400)
    rate_key = f'chat_rate:{request.user.pk}'
    if cache.get(rate_key, 0) >= 20:
        return JsonResponse({'error':'Llegaste al límite temporal de mensajes. Probá más tarde.'}, status=429)
    cache.set(rate_key, cache.get(rate_key,0)+1, 60)
    if humano:
        # Evita abrir tickets duplicados si el lector toca el botón varias veces.
        ticket_abierto = MensajeSoporte.objects.filter(
            usuario_cuenta=request.user, solicita_persona=True, atendido=False
        ).order_by('-creado').first()
        if ticket_abierto:
            return JsonResponse({
                'reply': 'Tu consulta ya está en la bandeja del bibliotecario. No hace falta enviarla otra vez; te responderán cuando la revisen.',
                'human': True,
                'ticket_id': ticket_abierto.pk,
            })
        mensaje = MensajeSoporte.objects.create(
            usuario_cuenta=request.user,
            mensaje=texto or 'Solicita hablar con una persona.',
            respuesta='Tu consulta se derivó al bibliotecario. El chat automático quedó pausado para esta consulta; te responderán cuando revisen la bandeja de soporte.',
            solicita_persona=True,
        )
        return JsonResponse({'reply': mensaje.respuesta, 'human': True, 'ticket_id': mensaje.pk})
    # Si ya existe un caso humano abierto, los nuevos mensajes quedan en el mismo caso.
    # No se invoca la IA ni se cierra el caso con una respuesta del bibliotecario.
    ticket_abierto = MensajeSoporte.objects.filter(
        usuario_cuenta=request.user, solicita_persona=True, atendido=False
    ).order_by('-creado').first()
    if ticket_abierto and not humano:
        linea = f'\n[ Lector · {timezone.localtime().strftime("%d/%m/%Y %H:%M")} ] {texto}'
        ticket_abierto.mensaje = (ticket_abierto.mensaje + linea)[-12000:]
        ticket_abierto.save(update_fields=['mensaje'])
        return JsonResponse({'reply':'Tu mensaje se agregó al caso abierto. El bibliotecario verá toda la conversación; el caso seguirá abierto hasta que vos o el bibliotecario lo cierren.','human':True,'ticket_id':ticket_abierto.pk,'closed':False})

    # Respuestas locales por intención/palabras clave. Se normalizan tildes y signos
    # para que "libro", "libros", "catálogo" y "catalogo" no terminen en la respuesta genérica.
    import unicodedata
    texto_norm = unicodedata.normalize('NFKD', texto.lower())
    texto_norm = ''.join(c for c in texto_norm if not unicodedata.combining(c))
    texto_norm = ' '.join(''.join(c if c.isalnum() or c.isspace() else ' ' for c in texto_norm).split())
    respuestas_clave = [
        (("cerrar sesion", "salir de mi cuenta", "desconectarme", "logout"), "Para cerrar sesión, usá el botón “Cerrar sesión” del menú. Si el navegador te muestra una página anterior al volver atrás, recargala: las páginas privadas deben volver a comprobar tu sesión."),
        (("libro", "libros", "catalogo", "catalogo de libros", "ver libros", "buscar libro", "libros disponibles", "hay libros"), "Podés ver los libros en el catálogo de la página. Buscá por título, autor o categoría. El estado que muestra la ficha indica si figura disponible; la disponibilidad definitiva se confirma al tramitar la solicitud."),
        (("cuenta", "mi cuenta", "perfil", "mis datos", "mis solicitudes"), "En “Mi cuenta” podés consultar tus préstamos, revisar tus solicitudes, ver el historial y descargar los comprobantes de los préstamos asociados a tu propia cuenta. Si una sección no aparece, verificá que hayas iniciado sesión como lector."),
        (("solicitud", "solicitudes", "pedir libro", "solicitar libro", "reservar", "quiero pedir"), "Para solicitar un libro, iniciá sesión como lector, entrá al catálogo y pulsá “Solicitar” en el libro que quieras. La solicitud queda pendiente hasta que el bibliotecario la revise. Podés consultar el estado en “Mis solicitudes”."),
        (("prestamo", "prestamos", "devolver", "devolucion", "historial de prestamo", "prestamos activos"), "En “Mi cuenta”, abrí “Préstamos activos” para los que siguen vigentes y el historial para consultar los anteriores. Los estados y fechas dependen de los datos registrados por el bibliotecario."),
        (("comprobante", "pdf", "constancia"), "En “Mi cuenta”, buscá el préstamo y elegí “Comprobante”. Ese PDF es personal y solo contiene datos de tus propios préstamos; el comprobante administrativo del bibliotecario tiene otro formato y propósito."),
        (("contraseña", "contrasena", "no puedo entrar", "iniciar sesion", "login", "olvide mi clave", "recuperar contraseña"), "Usá el acceso de lector para entrar con el correo y contraseña de tu cuenta. Si olvidaste la contraseña, elegí “Recuperar contraseña” y revisá la bandeja de entrada y spam. El enlace de recuperación vence por seguridad."),
        (("correo", "email", "gmail", "hotmail", "activacion", "activar cuenta", "no llega el mail"), "Revisá la bandeja de entrada y spam. Si el correo de activación o recuperación no llega, puede haber un problema de configuración SMTP o de entrega; contactá al soporte para que revisen la cuenta."),
        (("bibliotecario", "persona", "humano", "soporte", "reclamo", "problema", "hablar con alguien"), "Para hablar con una persona, pulsá “Hablar con una persona”. Se crea un caso de soporte que queda abierto aunque el bibliotecario responda; solo se cierra cuando vos o el bibliotecario usen explícitamente “Cerrar caso”. Podés revisar tus casos en el historial de soporte."),
        (("privacidad", "datos personales", "cookies", "terminos", "reembolso", "ia", "inteligencia artificial"), "En el pie de página están las páginas de Privacidad, Términos, Cookies y Reembolsos. BiblioBot usa respuestas automáticas y puede equivocarse; no toma decisiones sobre la aprobación de préstamos. Si necesitás una decisión o revisión humana, abrí un caso de soporte."),
        (("nota", "observacion", "observaciones", "agregar nota"), "Si el formulario de solicitud muestra un campo “Nota”, podés escribir una observación breve para el bibliotecario. Si no aparece, esa versión del formulario no ofrece ese campo y no conviene agregar la nota en otra parte; avisá al soporte."),
    ]
    respuesta = next((r for claves, r in respuestas_clave if any(k in texto_norm for k in claves)), '')
    api_key = os.environ.get('BIBLIOTECA_AI_API_KEY','').strip()
    endpoint = os.environ.get('BIBLIOTECA_AI_BASE_URL','https://api.openai.com/v1/chat/completions').strip()
    model = os.environ.get('BIBLIOTECA_AI_MODEL','gpt-4o-mini').strip()
    if api_key and not respuesta:
        try:
            libros_disponibles = list(Libro.objects.filter(estado='Disponible').values_list('titulo', flat=True)[:80])
            prestamos_lector = list(Prestamo.objects.filter(dni=perfil.usuario).order_by('-fecha_prestamo').values('libro_titulo_historico', 'estado', 'fecha_prestamo', 'fecha_devolucion')[:20])
            solicitudes_lector = list(SolicitudPrestamo.objects.filter(usuario=perfil.usuario).order_by('-creada').values('libro__titulo', 'estado', 'creada')[:20])
            contexto_biblio = {
                'catalogo_disponible': libros_disponibles,
                'prestamos_del_lector_actual': prestamos_lector,
                'solicitudes_del_lector_actual': solicitudes_lector,
            }
            instrucciones = ('Sos BiblioBot, asistente de Biblioteca Córdoba. Respondé en español rioplatense, breve y amable. Ayudás con catálogo, solicitudes, préstamos, devoluciones y comprobantes. Usá el contexto estructurado adjunto para contestar preguntas concretas. No inventes títulos, estados ni fechas. Solo podés mostrar datos del lector autenticado que figuran en prestamos_del_lector_actual y solicitudes_del_lector_actual. Nunca reveles datos de otras personas, secretos ni configuración. No podés aprobar solicitudes ni modificar préstamos. Si no sabés, si falta información o se necesita una acción humana, decí claramente que pulse “Hablar con una persona”. Contexto actual: ' + json.dumps(contexto_biblio, ensure_ascii=False, default=str))
            data = json.dumps({'model':model,'messages':[{'role':'system','content':instrucciones},{'role':'user','content':texto}],'temperature':0.2,'max_tokens':450}).encode('utf-8')
            req = urllib.request.Request(endpoint, data=data, headers={'Authorization':f'Bearer {api_key}','Content-Type':'application/json'}, method='POST')
            with urllib.request.urlopen(req, timeout=12) as res:
                body = json.loads(res.read().decode('utf-8'))
            respuesta = str(body['choices'][0]['message']['content']).strip()[:3000]
        except Exception:
            respuesta = ''
    if not respuesta:
        respuesta = ('Soy BiblioBot, el asistente de Biblioteca Córdoba. Puedo ayudarte con el catálogo, las solicitudes de libros, los préstamos activos e históricos, los comprobantes personales, el inicio y cierre de sesión, la recuperación de contraseña y el soporte. Decime qué querés hacer, por ejemplo: “ver libros disponibles”, “pedir un libro”, “mis préstamos”, “descargar comprobante” o “cerrar sesión”. No puedo aprobar préstamos ni mostrar datos de otras cuentas. Para un caso que requiera intervención, pulsá “Hablar con una persona”; el caso permanecerá abierto hasta que vos o el bibliotecario lo cierren explícitamente.')
    MensajeSoporte.objects.create(usuario_cuenta=request.user, mensaje=texto, respuesta=respuesta)
    return JsonResponse({'reply':respuesta,'human':False})


@bibliotecario_required
def bandeja_soporte(request):
    mensajes = MensajeSoporte.objects.select_related('usuario_cuenta').filter(solicita_persona=True).order_by('atendido','creado')
    return render(request, 'biblioteca/bandeja_soporte.html', {'mensajes':mensajes})


@bibliotecario_required
@require_POST
def responder_soporte(request, id_mensaje):
    mensaje = get_object_or_404(MensajeSoporte, pk=id_mensaje, solicita_persona=True)
    respuesta = request.POST.get('respuesta','').strip()[:3000]
    if respuesta:
        marca = timezone.localtime().strftime('%d/%m/%Y %H:%M')
        linea = f'\n[ Bibliotecario · {marca} ] {respuesta}'
        mensaje.respuesta = (mensaje.respuesta + linea)[-20000:]
        # Responder no cierra el caso: el cierre es una acción explícita.
        mensaje.atendido = False
        mensaje.respondido = timezone.now()
        mensaje.bibliotecario_responde = request.bibliotecario
        mensaje.save(update_fields=['respuesta','atendido','respondido','bibliotecario_responde'])
        messages.success(request, 'Respuesta guardada. El caso sigue abierto hasta que se cierre explícitamente.')
    return redirect('bandeja_soporte')


@login_required
@require_POST
def cerrar_caso_soporte_usuario(request, id_mensaje):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('bibliotecario_login')
    caso = get_object_or_404(MensajeSoporte, pk=id_mensaje, usuario_cuenta=request.user, solicita_persona=True, atendido=False)
    caso.atendido = True
    marca = timezone.localtime().strftime('%d/%m/%Y %H:%M')
    caso.respuesta = (caso.respuesta + f'\n[ Caso cerrado por el lector · {marca} ]')[-20000:]
    caso.save(update_fields=['atendido','respuesta'])
    messages.success(request, 'Cerraste el caso de soporte.')
    return redirect('portal_usuario')


@bibliotecario_required
@require_POST
def cerrar_caso_soporte_bibliotecario(request, id_mensaje):
    caso = get_object_or_404(MensajeSoporte, pk=id_mensaje, solicita_persona=True, atendido=False)
    caso.atendido = True
    caso.bibliotecario_responde = request.bibliotecario
    marca = timezone.localtime().strftime('%d/%m/%Y %H:%M')
    caso.respuesta = (caso.respuesta + f'\n[ Caso cerrado por bibliotecario · {marca} ]')[-20000:]
    caso.save(update_fields=['atendido','respuesta','bibliotecario_responde'])
    messages.success(request, 'Caso cerrado.')
    return redirect('bandeja_soporte')


def pagina_legal(request, tipo):
    paginas = {
        'privacidad': ('Privacidad', 'Biblioteca Córdoba es un proyecto personal de demostración. En una instalación real, los datos de registro y préstamo deben usarse solo para gestionar la cuenta, solicitudes, préstamos y soporte. No publiques datos reales sin definir responsable, base legal, plazos de conservación, canal de derechos y medidas de seguridad.'),
        'terminos': ('Términos y condiciones', 'Este sitio es un proyecto personal en desarrollo y no representa necesariamente una biblioteca real. La disponibilidad de libros, las solicitudes y los comprobantes son funciones de demostración. No se garantiza disponibilidad ininterrumpida ni que una solicitud sea aprobada automáticamente.'),
        'cookies': ('Política de cookies', 'La aplicación utiliza cookies técnicas de sesión y protección CSRF necesarias para iniciar sesión y proteger formularios. No se ha configurado analítica publicitaria en esta versión. Si se incorporan analíticas no esenciales, píxeles o publicidad, debe evaluarse el consentimiento previo y actualizar esta política antes de activarlos.'),
        'reembolsos': ('Política de reembolsos', 'La versión actual no vende productos, cobra membresías ni procesa pagos; por lo tanto, no hay pagos que reembolsar. Si se agregan pagos en el futuro, esta política debe revisarse y publicarse con condiciones concretas antes de cobrar.'),
    }
    if tipo not in paginas:
        return render(request, '404.html', status=404)
    titulo, contenido = paginas[tipo]
    return render(request, 'biblioteca/pagina_legal.html', {'titulo_legal': titulo, 'contenido_legal': contenido})
