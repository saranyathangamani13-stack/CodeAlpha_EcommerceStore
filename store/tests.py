from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Order, Product

User = get_user_model()


class StorefrontTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test lamp',
            slug='test-lamp',
            category='Home',
            description='A useful test product.',
            price=Decimal('24.00'),
            image_url='https://example.com/lamp.jpg',
            stock=5,
        )
        self.user = User.objects.create_user(username='shopper', password='long-test-password-123')

    def test_home_page_and_product_detail_render(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test lamp')

        detail = self.client.get(reverse('product_detail', args=[self.product.slug]))
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, '$24.00')

    def test_user_can_register_and_login(self):
        register_response = self.client.post(reverse('register'), {
            'username': 'newshopper',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(register_response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newshopper').exists())

        self.client.logout()
        login_response = self.client.post(reverse('login'), {
            'username': 'newshopper',
            'password': 'StrongPass123!',
        })
        self.assertEqual(login_response.status_code, 302)

    def test_product_can_be_added_to_session_cart(self):
        response = self.client.post(
            reverse('product_detail', args=[self.product.slug]),
            {'quantity': 2},
        )
        self.assertRedirects(response, reverse('cart'))
        cart_response = self.client.get(reverse('cart'))
        self.assertContains(cart_response, 'Test lamp')
        self.assertEqual(self.client.session['cart'][str(self.product.id)], 2)

    def test_invalid_cart_quantity_is_ignored_safely(self):
        session = self.client.session
        session['cart'] = {str(self.product.id): 'bad-value'}
        session.save()

        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your bag is empty')

    def test_checkout_creates_order_and_decrements_stock(self):
        self.client.force_login(self.user)
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()

        response = self.client.post(reverse('checkout'), {
            'full_name': 'Test Shopper',
            'email': 'shopper@example.com',
            'shipping_address': '12 Test Street',
            'city': 'Example City',
            'postal_code': '12345',
        })

        order = Order.objects.get(user=self.user)
        self.assertRedirects(response, reverse('order_detail', args=[order.reference]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)
        self.assertEqual(order.items.get().quantity, 2)
        self.assertEqual(order.total, Decimal('48.00'))
        self.assertEqual(self.client.session['cart'], {})

    def test_order_detail_is_private_to_owner(self):
        self.client.force_login(self.user)
        order = Order.objects.create(
            user=self.user,
            full_name='Test Shopper',
            email='shopper@example.com',
            shipping_address='12 Test Street',
            city='Example City',
            postal_code='12345',
        )

        other_user = User.objects.create_user(username='other', password='long-test-password-123')
        self.client.force_login(other_user)
        response = self.client.get(reverse('order_detail', args=[order.reference]))
        self.assertEqual(response.status_code, 404)