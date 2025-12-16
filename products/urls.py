from django.urls import path
from .views import ProductListCreateView, ProductDetailView

# URL patterns for product listing, creation, retrieval, updating, and deletion
urlpatterns = [
    path('products/', ProductListCreateView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
]
