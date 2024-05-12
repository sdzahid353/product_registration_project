from django.urls import path
from .views import ProductRegistrationView, ProductListView, ProductRetrieveUpdateDestroyView

urlpatterns = [
    path('products/register/', ProductRegistrationView.as_view(), name='product-registration'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
]
