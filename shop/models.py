import random
import string

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def rand_slug() -> str:
    """
    Generate a random string of lowercase letters and digits of length 3.
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

class Category(models.Model):
    """
    A model representing a category in a product catalog.
    """

    name = models.CharField('Категория', max_length=250, db_index=True)
    parent = models.ForeignKey(
        'self',on_delete=models.CASCADE, related_name='children', null=True,blank=True
        )
    slug =models.SlugField('URL', max_length=250, unique=True, null= False, editable=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        unique_together = (['name','parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        """
        Returns a string representation of the category, in the form of a nested tree.
        """
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '>'.join(full_path[::-1])
    
    def save(self, *args, **kwargs):
        """
        Saves the model instance to the database.
        """
        if not self.slug:
            self.slug = slugify(
                rand_slug() + '-PickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("shop:category-list", args=[str(self.slug)])
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField('Название', max_length=250)
    brand = models.CharField('Бренд', max_length=250)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField('URL', max_length=250)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField('Изображение', upload_to='products/products/%Y/%m/%d')
    available = models.BooleanField('В наличии', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("shop:product-detail", args=[str(self.slug)])
    
class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Returns a queryset of products that are available.

        Returns:
            QuerySet: A queryset of products that are available.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):

    objects = ProductManager()

    class Meta:
        proxy = True

        
        