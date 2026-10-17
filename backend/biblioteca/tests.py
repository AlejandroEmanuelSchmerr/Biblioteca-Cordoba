from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Usuario, Libro, Prestamo, PerfilBiblioteca, Bibliotecario


class BibliotecaTests(TestCase):

    def setUp(self):
        """
        Datos que se crean antes de cada prueba.
        """

        # Usuario de la biblioteca
        self.usuario = Usuario.objects.create(
            dni="40123456",
            nombre="Juan",
            apellido="Perez",
            telefono="351123456",
            email="juan@test.com"
        )

        # Libro de prueba
        self.libro = Libro.objects.create(
            titulo="Clean Code",
            autor="Robert Martin",
            editorial="Prentice Hall",
            anio=2008,
            categoria="Programacion"
        )

        # Usuario de Django para las pruebas de autenticación
        self.usuario_sistema = User.objects.create_user(
            username="testadmin",
            password="TestPassword123",
            is_staff=True
        )

        # Las vistas del personal usan una identidad independiente en Bibliotecario,
        # no una cuenta auth.User marcada como staff.
        self.bibliotecario = Bibliotecario.objects.create(
            username="bibliotecario_test", nombre="Biblio", apellido="Prueba",
            email="bibliotecario@test.com", activo=True,
            password="!"
        )
        self.bibliotecario.set_password("TestPassword123")
        self.bibliotecario.save()
        session = self.client.session
        session["bibliotecario_id"] = self.bibliotecario.pk
        session.save()

    # =========================================================
    # 1. CREAR USUARIO
    # =========================================================

    def test_crear_usuario(self):
        """
        Comprueba que Django pueda crear un usuario
        correctamente.
        """

        self.assertEqual(
            Usuario.objects.count(),
            1
        )

        usuario = Usuario.objects.get(
            dni="40123456"
        )

        self.assertEqual(
            usuario.nombre,
            "Juan"
        )

        self.assertEqual(
            usuario.apellido,
            "Perez"
        )

        self.assertEqual(
            usuario.email,
            "juan@test.com"
        )

    # =========================================================
    # 2. CREAR LIBRO
    # =========================================================

    def test_crear_libro(self):
        """
        Comprueba que un libro nuevo comience
        como Disponible.
        """

        self.assertEqual(
            Libro.objects.count(),
            1
        )

        libro = Libro.objects.get(
            titulo="Clean Code"
        )

        self.assertEqual(
            libro.titulo,
            "Clean Code"
        )

        self.assertEqual(
            libro.autor,
            "Robert Martin"
        )

        self.assertEqual(
            libro.estado,
            "Disponible"
        )

    # =========================================================
    # 3. CREAR PRESTAMO
    # =========================================================

    def test_crear_prestamo(self):
        """
        Comprueba que un usuario pueda realizar
        un préstamo de un libro disponible.
        """

        prestamo = Prestamo.objects.create(
            dni=self.usuario,
            id_libro=self.libro
        )

        self.assertEqual(
            Prestamo.objects.count(),
            1
        )

        self.assertEqual(
            prestamo.dni,
            self.usuario
        )

        self.assertEqual(
            prestamo.id_libro,
            self.libro
        )

        self.assertEqual(
            prestamo.estado,
            "Activo"
        )

    # =========================================================
    # 4. LIBRO PASA A PRESTADO
    # =========================================================

    def test_libro_pasa_a_prestado_al_crear_prestamo(self):
        """
        Comprueba el estado del libro después
        de realizar un préstamo.
        """

        prestamo = Prestamo.objects.create(
            dni=self.usuario,
            id_libro=self.libro
        )

        self.libro.estado = "Prestado"
        self.libro.save()

        self.libro.refresh_from_db()

        self.assertEqual(
            prestamo.estado,
            "Activo"
        )

        self.assertEqual(
            self.libro.estado,
            "Prestado"
        )

    # =========================================================
    # 5. IMPEDIR PRESTAMO DUPLICADO
    # =========================================================

    def test_no_permitir_prestamo_duplicado(self):
        """
        Comprueba que no se pueda realizar un segundo
        préstamo activo sobre el mismo libro.
        """

        Prestamo.objects.create(
            dni=self.usuario,
            id_libro=self.libro
        )

        self.libro.estado = "Prestado"
        self.libro.save()

        with self.assertRaises(ValidationError):
            Prestamo.objects.create(
                dni=self.usuario,
                id_libro=self.libro
            )

    # =========================================================
    # 6. DEVOLVER LIBRO
    # =========================================================

    def test_devolucion_libro(self):
        """
        Comprueba que al devolver un préstamo:

        Préstamo -> Devuelto
        Libro -> Disponible
        """

        prestamo = Prestamo.objects.create(
            dni=self.usuario,
            id_libro=self.libro
        )

        self.libro.estado = "Prestado"
        self.libro.save()

        prestamo.estado = "Devuelto"
        prestamo.save()

        self.libro.estado = "Disponible"
        self.libro.save()

        prestamo.refresh_from_db()
        self.libro.refresh_from_db()

        self.assertEqual(
            prestamo.estado,
            "Devuelto"
        )

        self.assertEqual(
            self.libro.estado,
            "Disponible"
        )

    # =========================================================
    # 7. FORMULARIO IMPIDE PRESTAMO DUPLICADO
    # =========================================================

    def test_formulario_impide_prestamo_duplicado(self):
        """
        Comprueba que PrestamoForm rechace un libro
        que ya está Prestado.
        """

        from .forms import PrestamoForm

        Prestamo.objects.create(
            dni=self.usuario,
            id_libro=self.libro
        )

        self.libro.estado = "Prestado"
        self.libro.save()

        form = PrestamoForm(
            data={
                "dni": self.usuario.dni,
                "id_libro": self.libro.id_libro
            }
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "id_libro",
            form.errors
        )

    # =========================================================
    # 8. VISTA PARA CREAR PRESTAMO
    # =========================================================

    def test_vista_crear_prestamo(self):
        """
        Comprueba el flujo real de la vista:

        Formulario
            ↓
        prestamo_crear
            ↓
        Préstamo Activo
            ↓
        Libro Prestado
        """

        respuesta = self.client.post(
            reverse("prestamo_nuevo"),
            {
                "dni": self.usuario.dni,
                "id_libro": self.libro.id_libro
            }
        )

        self.assertRedirects(
            respuesta,
            reverse("prestamo_lista")
        )

        self.assertEqual(
            Prestamo.objects.count(),
            1
        )

        prestamo = Prestamo.objects.first()

        self.assertEqual(
            prestamo.estado,
            "Activo"
        )

        self.libro.refresh_from_db()

        self.assertEqual(
            self.libro.estado,
            "Prestado"
        )

    # =========================================================
    # 9. VISTA IMPIDE PRESTAMO DUPLICADO
    # =========================================================

    def test_vista_impide_prestamo_duplicado(self):
        """
        Comprueba que la vista real no permita
        prestar nuevamente un libro Prestado.
        """

        respuesta = self.client.post(
            reverse("prestamo_nuevo"),
            {
                "dni": self.usuario.dni,
                "id_libro": self.libro.id_libro
            }
        )

        self.assertRedirects(
            respuesta,
            reverse("prestamo_lista")
        )

        self.assertEqual(
            Prestamo.objects.count(),
            1
        )

        segunda_respuesta = self.client.post(
            reverse("prestamo_nuevo"),
            {
                "dni": self.usuario.dni,
                "id_libro": self.libro.id_libro
            }
        )

        self.assertEqual(
            segunda_respuesta.status_code,
            200
        )

        self.assertEqual(
            Prestamo.objects.count(),
            1
        )

    # =========================================================
    # 10. VISTA DE DEVOLUCION
    # =========================================================

    def test_vista_devolver_prestamo(self):
        """
        Comprueba el flujo real de devolución:

        Préstamo Activo
            ↓
        Devolver
            ↓
        Préstamo Devuelto
            ↓
        Libro Disponible
        """

        respuesta = self.client.post(
            reverse("prestamo_nuevo"),
            {
                "dni": self.usuario.dni,
                "id_libro": self.libro.id_libro
            }
        )

        self.assertRedirects(
            respuesta,
            reverse("prestamo_lista")
        )

        prestamo = Prestamo.objects.first()

        self.libro.refresh_from_db()

        self.assertEqual(
            prestamo.estado,
            "Activo"
        )

        self.assertEqual(
            self.libro.estado,
            "Prestado"
        )

        respuesta_devolucion = self.client.post(
            reverse(
                "prestamo_devolver",
                args=[prestamo.id_prestamo]
            )
        )

        self.assertRedirects(
            respuesta_devolucion,
            reverse("prestamo_lista")
        )

        prestamo.refresh_from_db()
        self.libro.refresh_from_db()

        self.assertEqual(
            prestamo.estado,
            "Devuelto"
        )

        self.assertIsNotNone(
            prestamo.fecha_devolucion
        )

        self.assertEqual(
            self.libro.estado,
            "Disponible"
        )

    # =========================================================
    # 11. VISTA CREAR USUARIO
    # =========================================================

    def test_vista_crear_usuario(self):
        """
        Comprueba que usuario_crear pueda registrar
        correctamente un usuario mediante POST.
        """

        respuesta = self.client.post(
            reverse("usuario_nuevo"),
            {
                "dni": "40999888",
                "nombre": "Maria",
                "apellido": "Gomez",
                "telefono": "351999888",
                "email": "maria@test.com"
            }
        )

        self.assertRedirects(
            respuesta,
            reverse("usuario_lista")
        )

        self.assertTrue(
            Usuario.objects.filter(
                dni="40999888"
            ).exists()
        )

    # =========================================================
    # 12. VISTA CREAR LIBRO
    # =========================================================

    def test_vista_crear_libro(self):
        """
        Comprueba que un libro creado mediante la vista
        quede Disponible.
        """

        respuesta = self.client.post(
            reverse("libro_nuevo"),
            {
                "titulo": "Python Crash Course",
                "autor": "Eric Matthes",
                "editorial": "No Starch Press",
                "anio": 2023,
                "categoria": "Programacion"
            }
        )

        self.assertRedirects(
            respuesta,
            reverse("libro_lista")
        )

        libro = Libro.objects.get(
            titulo="Python Crash Course"
        )

        self.assertEqual(
            libro.estado,
            "Disponible"
        )

    # =========================================================
    # 13. ERROR DNI CON LETRAS
    # =========================================================

    def test_dni_no_acepta_letras(self):
        """
        Comprueba que el formulario de usuario
        rechace un DNI que contenga letras.
        """

        from .forms import UsuarioForm

        form = UsuarioForm(
            data={
                "dni": "40ABC123",
                "nombre": "Pedro",
                "apellido": "Gomez",
                "telefono": "351123456",
                "email": "pedro@test.com"
            }
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "dni",
            form.errors
        )

        self.assertIn(
            "El DNI debe contener solo números",
            form.errors["dni"]
        )

    # =========================================================
    # 14. ERROR AÑO MAYOR AL ACTUAL
    # =========================================================

    def test_anio_no_puede_ser_mayor_al_actual(self):
        """
        Comprueba que el formulario de libro
        rechace un año mayor al actual.
        """

        from .forms import LibroForm

        form = LibroForm(
            data={
                "titulo": "Libro Futuro",
                "autor": "Autor Test",
                "editorial": "Editorial Test",
                "anio": timezone.localdate().year + 1,
                "categoria": "Programacion"
            }
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "anio",
            form.errors
        )

        self.assertIn(
            "El año no puede ser mayor al actual",
            form.errors["anio"]
        )

    # =========================================================
    # 15. ERROR LIBRO NO DISPONIBLE
    # =========================================================

    def test_formulario_rechaza_libro_no_disponible(self):
        """
        Comprueba que el formulario rechace un libro
        que se encuentra Prestado.
        """

        from .forms import PrestamoForm

        self.libro.estado = "Prestado"
        self.libro.save()

        form = PrestamoForm(
            data={
                "dni": self.usuario.dni,
                "id_libro": self.libro.id_libro
            }
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "id_libro",
            form.errors
        )

        self.assertTrue(
            any(
                "No se puede prestar" in error
                for error in form.errors["id_libro"]
            )
        )

    # =========================================================
    # 16. MENSAJE CREAR USUARIO
    # =========================================================

    def test_mensaje_usuario_creado(self):
        """
        Comprueba que al crear un usuario
        aparezca el mensaje correspondiente.
        """

        respuesta = self.client.post(
            reverse("usuario_nuevo"),
            {
                "dni": "40999888",
                "nombre": "Maria",
                "apellido": "Gomez",
                "telefono": "351999888",
                "email": "maria@test.com"
            },
            follow=True
        )

        self.assertEqual(
            respuesta.status_code,
            200
        )

        self.assertContains(
            respuesta,
            "Usuario creado correctamente."
        )

    # =========================================================
    # 17. MENSAJE CREAR PRESTAMO
    # =========================================================

    def test_mensaje_prestamo_creado(self):
        """
        Comprueba que al crear un préstamo
        aparezca el mensaje correspondiente.
        """

        respuesta = self.client.post(
            reverse("prestamo_nuevo"),
            {
                "dni": self.usuario.dni,
                "id_libro": self.libro.id_libro
            },
            follow=True
        )

        self.assertEqual(
            respuesta.status_code,
            200
        )

        self.assertContains(
            respuesta,
            "Préstamo registrado"
        )

    # =========================================================
    # 18. MENSAJE DEVOLVER LIBRO
    # =========================================================

    def test_mensaje_libro_devuelto(self):
        """
        Comprueba que al devolver un préstamo
        aparezca el mensaje correspondiente.
        """

        prestamo = Prestamo.objects.create(
            dni=self.usuario,
            id_libro=self.libro
        )

        self.libro.estado = "Prestado"
        self.libro.save()

        respuesta = self.client.post(
            reverse(
                "prestamo_devolver",
                args=[prestamo.id_prestamo]
            ),
            follow=True
        )

        self.assertEqual(
            respuesta.status_code,
            200
        )

        self.assertContains(
            respuesta,
            "devuelto correctamente"
        )

    # =========================================================
    # 19. MENSAJE PRÉSTAMO YA DEVUELTO
    # =========================================================

    def test_mensaje_prestamo_ya_devuelto(self):
        """
        Comprueba que al intentar devolver nuevamente
        un préstamo ya devuelto aparezca un aviso.
        """

        prestamo = Prestamo.objects.create(
            dni=self.usuario,
            id_libro=self.libro
        )

        self.libro.estado = "Prestado"
        self.libro.save()

        prestamo.estado = "Devuelto"
        prestamo.fecha_devolucion = timezone.now().date()
        prestamo.save()

        self.libro.estado = "Disponible"
        self.libro.save()

        respuesta = self.client.post(
            reverse(
                "prestamo_devolver",
                args=[prestamo.id_prestamo]
            ),
            follow=True
        )

        self.assertEqual(
            respuesta.status_code,
            200
        )

        self.assertContains(
            respuesta,
            "ya fue devuelto"
        )
        
    # =========================================================
    # 20. VISTA PROTEGIDA SIN AUTENTICACION
    # =========================================================

    def test_usuario_lista_requiere_login(self):
        """
        Comprueba que un usuario no autenticado
        no pueda acceder al listado de usuarios.
        """

        self.client.logout()

        respuesta = self.client.get(
            reverse("usuario_lista")
        )

        self.assertEqual(
            respuesta.status_code,
            302
        )

        self.assertIn(
            "/login/",
            respuesta.url
        )

    # =========================================================
    # 21. LOGIN CORRECTO
    # =========================================================

    def test_login_correcto(self):
        """
        Comprueba que un usuario pueda iniciar sesión
        correctamente.
        """

        self.client.logout()

        # El login de lectores acepta cuentas no-staff; las cuentas de personal
        # usan /bibliotecario/login/ y el superusuario usa /admin/.
        lector = User.objects.create_user(
            username="lector_test",
            password="TestPassword123",
            email="lector_test@example.com",
            is_staff=False,
            is_superuser=False,
            is_active=True,
        )
        # Una cuenta lectora real siempre queda vinculada a su ficha de biblioteca.
        # El test debe reflejar el flujo de registro real y no crear una cuenta huérfana.
        ficha_lectora = Usuario.objects.create(
            dni="40123457",
            nombre="Lector",
            apellido="Prueba",
            telefono="351123457",
            email="lector_test@example.com",
        )
        PerfilBiblioteca.objects.create(cuenta=lector, usuario=ficha_lectora)
        respuesta = self.client.post(
            reverse("login"),
            {"username": "lector_test", "password": "TestPassword123"}
        )

        self.assertRedirects(respuesta, reverse("portal_usuario"))
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_login_lector_redirige_a_portal_con_ficha_vinculada(self):
        """El acceso lector lleva al portal si la cuenta tiene ficha asociada."""
        self.client.logout()
        lector = User.objects.create_user(
            username="lector_portal_test", password="TestPassword123",
            email="lector_portal@example.com", is_staff=False,
            is_superuser=False, is_active=True,
        )
        ficha = Usuario.objects.create(
            dni="40123458", nombre="Lector", apellido="Portal",
            telefono="351123458", email="lector_portal@example.com",
        )
        PerfilBiblioteca.objects.create(cuenta=lector, usuario=ficha)
        respuesta = self.client.post(reverse("login"), {
            "username": "lector_portal_test", "password": "TestPassword123"
        })
        self.assertRedirects(respuesta, reverse("portal_usuario"))
        portal = self.client.get(reverse("portal_usuario"))
        self.assertEqual(portal.status_code, 200)

    # =========================================================
    # 22. LOGIN INCORRECTO
    # =========================================================

    def test_login_incorrecto(self):
        """
        Comprueba que no se pueda iniciar sesión
        con una contraseña incorrecta.
        """

        self.client.logout()

        respuesta = self.client.post(
            reverse("login"),
            {
                "username": "testadmin",
                "password": "ContraseñaIncorrecta123"
            }
        )

        self.assertEqual(
            respuesta.status_code,
            200
        )

        self.assertContains(
            respuesta,
            "Usuario o contraseña incorrectos"
        )

        self.assertNotIn(
            "_auth_user_id",
            self.client.session
        )

    # =========================================================
    # 23. LOGOUT
    # =========================================================

    def test_logout(self):
        """
        Comprueba que el usuario pueda cerrar sesión.
        """

        respuesta = self.client.get(
            reverse("logout")
        )

        self.assertRedirects(
            respuesta,
            reverse("bibliotecario_login")
        )

        self.assertNotIn(
            "_auth_user_id",
            self.client.session
        )
    # =========================================================
    # 24. PANEL PRINCIPAL Y ESTADISTICAS
    # =========================================================

    def test_inicio_muestra_estadisticas(self):
        """
        Comprueba que el panel principal muestre las estadísticas
        básicas del sistema para el usuario autenticado.
        """

        respuesta = self.client.get(reverse("inicio"))

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["total_usuarios"], 1)
        self.assertEqual(respuesta.context["total_libros"], 1)
        self.assertEqual(respuesta.context["libros_disponibles"], 1)
        self.assertEqual(respuesta.context["prestamos_activos"], 0)
        self.assertContains(respuesta, "Usuarios registrados")
        self.assertContains(respuesta, "Libros disponibles")
        self.assertContains(respuesta, "Préstamos activos")

    # =========================================================
    # 25. INICIO REQUIERE LOGIN
    # =========================================================

    def test_inicio_requiere_login(self):
        """
        Comprueba que una persona no autenticada no pueda acceder
        al panel principal.
        """

        self.client.logout()

        respuesta = self.client.get(reverse("inicio"))

        self.assertEqual(respuesta.status_code, 302)
        self.assertIn("/login/", respuesta.url)

    # =========================================================
    # 26. PROTEGER HISTORIAL AL ELIMINAR USUARIO
    # =========================================================

    def test_no_eliminar_usuario_con_prestamos(self):
        """
        Comprueba que un usuario con historial de préstamos no pueda
        eliminarse desde la vista.
        """

        Prestamo.objects.create(
            dni=self.usuario,
            id_libro=self.libro
        )

        respuesta = self.client.post(
            reverse("usuario_eliminar", args=[self.usuario.dni])
        )

        self.assertRedirects(respuesta, reverse("usuario_lista"))
        self.assertTrue(
            Usuario.objects.filter(dni=self.usuario.dni).exists()
        )
        self.assertEqual(Prestamo.objects.count(), 1)

    # =========================================================
    # 27. PROTEGER HISTORIAL AL ELIMINAR LIBRO
    # =========================================================

    def test_no_eliminar_libro_con_prestamos(self):
        """
        Comprueba que un libro con historial de préstamos no pueda
        eliminarse desde la vista.
        """

        Prestamo.objects.create(
            dni=self.usuario,
            id_libro=self.libro
        )

        respuesta = self.client.post(
            reverse("libro_eliminar", args=[self.libro.id_libro])
        )

        self.assertRedirects(respuesta, reverse("libro_lista"))
        self.assertTrue(
            Libro.objects.filter(id_libro=self.libro.id_libro).exists()
        )
        self.assertEqual(Prestamo.objects.count(), 1)


class ValidacionesYSeguridadTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(dni="40123456", nombre="Juan", apellido="Perez", telefono="351123456", email="juan@test.com")
        self.libro = Libro.objects.create(titulo="Clean Code", autor="Robert Martin", editorial="Prentice Hall", anio=2008, categoria="Programacion")
        User.objects.create_user(username="testadmin", password="TestPassword123", is_staff=True)
        self.bibliotecario = Bibliotecario.objects.create(
            username="bibliotecario_test", nombre="Biblio", apellido="Prueba",
            email="bibliotecario@test.com", activo=True, password="!"
        )
        self.bibliotecario.set_password("TestPassword123")
        self.bibliotecario.save()
        session = self.client.session
        session["bibliotecario_id"] = self.bibliotecario.pk
        session.save()


    def test_dni_debe_tener_exactamente_8_digitos(self):
        from .forms import UsuarioForm
        for dni in ["1234567", "123456789", "12ABC678"]:
            form = UsuarioForm(data={
                "dni": dni,
                "nombre": "Ana",
                "apellido": "Lopez",
                "telefono": "3511234567",
                "email": "ana123@gmail.com",
            })
            self.assertFalse(form.is_valid())
            self.assertIn("dni", form.errors)

    def test_telefono_no_supera_12_digitos(self):
        from .forms import UsuarioForm
        form = UsuarioForm(data={
            "dni": "40987654",
            "nombre": "Ana",
            "apellido": "Lopez",
            "telefono": "1234567890123",
            "email": "ana123@gmail.com",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("telefono", form.errors)

    def test_gmail_sin_numero_tambien_es_valido(self):
        from .forms import UsuarioForm
        form = UsuarioForm(data={
            "dni": "40987654",
            "nombre": "Ana",
            "apellido": "Lopez",
            "telefono": "3511234567",
            "email": "analopez@gmail.com",
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_gmail_con_numero_es_valido(self):
        from .forms import UsuarioForm
        form = UsuarioForm(data={
            "dni": "40987654",
            "nombre": "Ana",
            "apellido": "Lopez",
            "telefono": "3511234567",
            "email": "ana123@gmail.com",
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_pagina_404_personalizada(self):
        response = self.client.get("/ruta-que-no-existe-123/")
        self.assertEqual(response.status_code, 404)

    def test_devolucion_no_acepta_get(self):
        prestamo = Prestamo.objects.create(dni=self.usuario, id_libro=self.libro)
        self.libro.estado = "Prestado"
        self.libro.save()
        response = self.client.get(reverse("prestamo_devolver", args=[prestamo.id_prestamo]))
        self.assertRedirects(response, reverse("prestamo_lista"))
        prestamo.refresh_from_db()
        self.assertEqual(prestamo.estado, "Activo")

    def test_no_eliminar_usuario_con_historial(self):
        Prestamo.objects.create(dni=self.usuario, id_libro=self.libro)
        response = self.client.post(reverse("usuario_eliminar", args=[self.usuario.dni]))
        self.assertRedirects(response, reverse("usuario_lista"))
        self.assertTrue(Usuario.objects.filter(dni=self.usuario.dni).exists())

    def test_no_eliminar_libro_con_historial(self):
        Prestamo.objects.create(dni=self.usuario, id_libro=self.libro)
        response = self.client.post(reverse("libro_eliminar", args=[self.libro.id_libro]))
        self.assertRedirects(response, reverse("libro_lista"))
        self.assertTrue(Libro.objects.filter(id_libro=self.libro.id_libro).exists())


class HistorialYComprobantesTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(dni='40123456', nombre='Juan', apellido='Perez', telefono='351123456', email='juan@test.com')
        self.libro = Libro.objects.create(titulo='Clean Code', autor='Robert Martin', editorial='Prentice Hall', anio=2008, categoria='Programacion')
        User.objects.create_user(username='testadmin', password='TestPassword123', is_staff=True)
        self.bibliotecario = Bibliotecario.objects.create(
            username='bibliotecario_test', nombre='Biblio', apellido='Prueba',
            email='bibliotecario@test.com', activo=True, password='!'
        )
        self.bibliotecario.set_password('TestPassword123')
        self.bibliotecario.save()
        session = self.client.session
        session['bibliotecario_id'] = self.bibliotecario.pk
        session.save()

    def test_libro_con_prestamo_devuelto_se_puede_eliminar_y_historial_se_conserva(self):
        prestamo = Prestamo.objects.create(dni=self.usuario, id_libro=self.libro, estado='Devuelto', fecha_devolucion=timezone.localdate())
        response = self.client.post(reverse('libro_eliminar', args=[self.libro.id_libro]))
        self.assertRedirects(response, reverse('libro_lista'))
        prestamo.refresh_from_db()
        self.assertIsNone(prestamo.id_libro)
        self.assertEqual(prestamo.libro_titulo_historico, 'Clean Code')
        self.assertEqual(prestamo.libro_mostrado, 'Clean Code')

    def test_historial_muestra_prestamos_devuelto(self):
        Prestamo.objects.create(dni=self.usuario, id_libro=self.libro, estado='Devuelto', fecha_devolucion=timezone.localdate())
        response = self.client.get(reverse('prestamo_historial'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clean Code')

    def test_comprobante_pdf_se_descarga(self):
        prestamo = Prestamo.objects.create(dni=self.usuario, id_libro=self.libro)
        response = self.client.get(reverse('prestamo_comprobante_pdf', args=[prestamo.id_prestamo]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment;', response['Content-Disposition'])
    def test_eliminar_usuario_inexistente_no_expone_error_interno(self):
        response = self.client.post(reverse('usuario_eliminar', args=['34222232']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('usuario_lista'))
        self.assertNotContains(response, 'No Usuario matches the given query', status_code=302)

    def test_dni_con_letras_no_es_valido_en_formulario(self):
        from .forms import UsuarioForm
        form = UsuarioForm(data={
            'dni': '12A45678', 'nombre': 'Ana', 'apellido': 'Pérez',
            'telefono': '351123456', 'email': 'ana123@example.com',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('dni', form.errors)

