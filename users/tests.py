from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings
from datetime import timedelta

User = get_user_model()


class UserModelAndSecurityTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_password = "AdminSecretPass123!"
        self.client_password = "ClientSecretPass123!"

        self.admin = User.objects.create_superuser(
            email="admin_test@tiendaonline.com",
            password=self.admin_password,
            first_name="Admin",
            last_name="Test",
            telefono="555-0001"
        )

        self.user = User.objects.create_user(
            email="cliente_test@tiendaonline.com",
            password=self.client_password,
            first_name="Cliente",
            last_name="Test",
            telefono="555-0002"
        )

    def test_custom_user_model_extra_field(self):
        """Verifica que el modelo use email como USERNAME_FIELD y posea el campo extra 'telefono'."""
        self.assertEqual(User.USERNAME_FIELD, 'email')
        self.assertEqual(self.user.telefono, "555-0002")
        self.assertEqual(self.admin.telefono, "555-0001")

    def test_access_token_lifetime_configured(self):
        """Verifica que el tiempo de vida del token de acceso esté configurado según las indicaciones."""
        self.assertIn('ACCESS_TOKEN_LIFETIME', settings.SIMPLE_JWT)
        self.assertEqual(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'], timedelta(minutes=60))

    def test_obtain_jwt_token(self):
        """Verifica la obtención de tokens JWT mediante POST a /api/v1/auth/token/ usando email."""
        response = self.client.post('/api/v1/auth/token/', {
            'email': 'cliente_test@tiendaonline.com',
            'password': self.client_password
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_me_endpoint_security_no_password_hash(self):
        """
        Corrección de seguridad 1:
        El endpoint /api/v1/auth/me/ NUNCA debe devolver el hash de la contraseña.
        Debe incluir el campo extra 'telefono'.
        """
        login_res = self.client.post('/api/v1/auth/token/', {
            'email': 'cliente_test@tiendaonline.com',
            'password': self.client_password
        }, format='json')
        token = login_res.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/v1/auth/me/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'cliente_test@tiendaonline.com')
        self.assertEqual(response.data['telefono'], '555-0002')
        # Verificar que NO aparezca la contraseña ni su hash
        self.assertNotIn('password', response.data)

    def test_users_crud_no_password_in_list_or_detail(self):
        """
        Corrección de seguridad 1:
        El listado y detalle de usuarios tampoco deben exponer el hash de la contraseña.
        """
        self.client.force_authenticate(user=self.admin)
        
        # Listado
        res_list = self.client.get('/api/v1/users/')
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        for user_data in res_list.data:
            self.assertNotIn('password', user_data)
            self.assertIn('telefono', user_data)

        # Detalle
        res_detail = self.client.get(f'/api/v1/users/{self.user.id}/')
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', res_detail.data)
        self.assertEqual(res_detail.data['telefono'], '555-0002')

    def test_edit_user_without_password_does_not_change_password(self):
        """
        Corrección de seguridad 2:
        Al actualizar un usuario sin enviar contraseña (PATCH), NO debe asignársele
        la contraseña del usuario que realiza la petición (el admin), y la contraseña original
        del usuario objetivo debe mantenerse intacta.
        """
        original_password_hash = self.user.password

        # El admin realiza una actualización parcial sin enviar contraseña
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(f'/api/v1/users/{self.user.id}/', {
            'telefono': '555-9999',
            'first_name': 'Carlos Editado'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)

        # Recargamos el usuario desde la base de datos
        self.user.refresh_from_db()
        self.assertEqual(self.user.telefono, '555-9999')
        self.assertEqual(self.user.first_name, 'Carlos Editado')

        # 1. El hash de la contraseña NO debe haber cambiado
        self.assertEqual(self.user.password, original_password_hash)

        # 2. El usuario objetivo NO debe tener la contraseña del admin
        self.assertNotEqual(self.user.password, self.admin.password)

        # 3. El usuario puede seguir autenticándose con su contraseña original
        self.client.force_authenticate(user=None)  # Limpiar sesión
        auth_response = self.client.post('/api/v1/auth/token/', {
            'email': 'cliente_test@tiendaonline.com',
            'password': self.client_password
        }, format='json')
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', auth_response.data)

    def test_edit_user_with_new_password_changes_password_securely(self):
        """
        Verifica que cuando SÍ se envía una nueva contraseña, esta se encripta
        y el usuario puede autenticarse con la nueva contraseña.
        """
        new_pass = "NewSuperPassword2026!"
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(f'/api/v1/users/{self.user.id}/', {
            'password': new_pass
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)

        # Recargamos el usuario
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.password, new_pass)  # Debe ser hash, no texto plano
        self.assertTrue(self.user.check_password(new_pass))

        # El usuario se autentica con la nueva contraseña
        self.client.force_authenticate(user=None)
        auth_res = self.client.post('/api/v1/auth/token/', {
            'email': 'cliente_test@tiendaonline.com',
            'password': new_pass
        }, format='json')
        self.assertEqual(auth_res.status_code, status.HTTP_200_OK)
