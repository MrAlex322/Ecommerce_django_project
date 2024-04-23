from django.urls import path

from .views import category_list, product_detail_view, product_view

app_name = 'shop'

urlpatterns = [
    path('', product_view, name='products'),
    path('<slug:slug>/', product_detail_view, name='product-detail'),
    path('search/<slug:slug>/', category_list, name='category-list'),
]
