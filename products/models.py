from django.db import models
from django.db.models import F, Func
from django.contrib.postgres.indexes import GinIndex

# Product model to store product information
class Product(models.Model):
    fields = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            # GIN index for general JSON queries (name filtering)
            GinIndex(fields=['fields'], name='product_fields_gin_idx'),
            # B-tree functional index for price range queries
            models.Index(
                Func(F('fields'), models.Value('price'), function='jsonb_extract_path_text', output_field=models.TextField()),
                name='product_price_idx'
            ),
        ]
