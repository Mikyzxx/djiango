from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Category, Product


class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electrónica')

    def test_create_category(self):
        """Prueba la creación exitosa de una nueva categoría."""
        response = self.client.post('/api/categories/', {'name': 'Ropa'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_list_categories(self):
        """Prueba que el endpoint liste correctamente las categorías existentes."""
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electrónica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            description='Laptop HP para desarrollo',
            price=15000.00,
            is_active=True
        )

    def test_create_product(self):
        """Prueba la creación de un nuevo producto asociado a una categoría."""
        response = self.client.post('/api/products/', {
            'name': 'Mouse',
            'category': self.category.id,
            'description': 'Mouse inalámbrico',
            'price': 500.00,
            'is_active': True
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_list_products(self):
        """Prueba que se listen correctamente los productos registrados."""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_product(self):
        """Prueba la actualización completa de los datos de un producto."""
        response = self.client.put(f'/api/products/{self.product.id}/', {
            'name': 'Laptop Pro',
            'category': self.category.id,
            'description': 'Laptop HP actualizada',
            'price': 18000.00,
            'is_active': True
        })
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop Pro')

    def test_delete_product(self):
        """Prueba la eliminación de un producto existente por su ID."""
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

    def test_precio_final_autenticado(self):
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_final', response.data)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 401)
