from django.db import models

# Product model to store product information
class Product(models.Model):
    fields = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
