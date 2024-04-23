from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, ProductProxy


class ProductView(TestCase):
    def test_get_product(self):
        """
        Test the get product view.
        """
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile('test_images.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='django')
        product_1 = Product.objects.create(title='Product 1', category=category, image=uploaded, slug='product-1')
        product_2 = Product.objects.create(title='Product 2', category=category, image=uploaded, slug='product-2')

        response = self.client.get(reverse('shop:products'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'].count(), 2)
        self.assertEqual(list(response.context['products']), [product_1, product_2])
        self.assertContains(response, product_1)
        self.assertContains(response, product_2)
        
class  ProductDetailViewTest(TestCase):
    def test__get_product_by_slug(self):
        """
        Test the get product view.
        """
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile('test_images.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='django')
        product_1 = Product.objects.create(title='Product 1', category=category, image=uploaded, slug='product-1')
        product_2 = Product.objects.create(title='Product 2', category=category, image=uploaded, slug='product-2')

        response = self.client.get(reverse('shop:products'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'].count(), 2)
        self.assertEqual(list(response.context['products']), [product_1, product_2])
        self.assertContains(response, product_1)
        self.assertContains(response, product_2)

class CategoryListViewTest(TestCase):
    """
    Test the get product view.
    """
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(
            name='Test Category', slug='test-category')
        self.product = ProductProxy.objects.create(
            title='Test Product', slug='test-product', category=self.category, image=uploaded)

    def test_status_code(self):
        """
        Test the status code of the response for the category list view.

        This function sends a GET request to the category list view with the specified category slug,
        and then checks the status code of the response. The expected status code is 200, indicating
        that the request was successful.
        """
        response = self.client.get(
            reverse('shop:category-list', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """
        Test that the correct template is used for the category list view.

        This test ensures that the correct template is used for the category list view,
        which is 'shop/category_list.html'.
        """
        response = self.client.get(
            reverse('shop:category-list', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/category_list.html')

    def test_context_data(self):
        """
        Test the context data of the category list view.

        This test ensures that the context data of the category list view contains the expected
        values, including the category and the products.
        """
        response = self.client.get(
            reverse('shop:category-list', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/category_list.html')
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'].first(), self.product)