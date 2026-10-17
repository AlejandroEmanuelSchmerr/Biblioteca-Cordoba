from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Bibliotecario


class RolesSeparadosTests(TestCase):
    def setUp(self):
        self.reader = User.objects.create_user(
            username='lector-test', password='PruebaSegura123!', is_active=True
        )
        self.staff_user = User.objects.create_user(
            username='staff-antiguo', password='NoUsar123!', is_staff=True
        )
        self.bibliotecario = Bibliotecario(
            username='bibliotecario-test',
            nombre='Ana',
            apellido='Prueba',
            email='ana@example.test',
            activo=True,
        )
        self.bibliotecario.set_password('ClaveSegura123!')
        self.bibliotecario.save()

    def test_bibliotecario_es_entidad_independiente(self):
        self.assertNotEqual(self.bibliotecario._meta.db_table, User._meta.db_table)
        self.assertTrue(self.bibliotecario.check_password('ClaveSegura123!'))
        self.assertFalse(self.bibliotecario.check_password('incorrecta'))

    def test_login_bibliotecario_no_depende_de_auth_user_staff(self):
        c = Client()
        response = c.post(
            reverse('bibliotecario_login'),
            {'username': 'bibliotecario-test', 'password': 'ClaveSegura123!'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('bibliotecario_id', c.session)
        self.assertNotIn('_auth_user_id', c.session)

    def test_cuenta_staff_de_django_no_autoriza_panel_bibliotecario(self):
        c = Client()
        c.force_login(self.staff_user)
        response = c.get(reverse('inicio'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/bibliotecario/login/', response.url)

    def test_login_personal_rechaza_usuario_de_auth_django_aunque_sea_staff(self):
        c = Client()
        response = c.post(
            reverse('bibliotecario_login'),
            {'username': 'staff-antiguo', 'password': 'NoUsar123!'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('bibliotecario_id', c.session)

    def test_lector_no_puede_entrar_al_panel_personal(self):
        c = Client()
        c.force_login(self.reader)
        response = c.get(reverse('inicio'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/bibliotecario/login/', response.url)