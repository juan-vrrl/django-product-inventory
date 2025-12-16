from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# View to handle listing and creating products
class ProductListCreateView(APIView):
    # Get all products
    def get(self, request):
        products = Product.objects.all()
        
        # Filter by name (exact match or partial)
        name = request.query_params.get('name')
        if name:
            products = products.filter(fields__name__icontains=name)
        
        # Filter by price range
        price_gte = request.query_params.get('price_gte')  # greater than or equal
        price_lte = request.query_params.get('price_lte')  # less than or equal
        
        if price_gte:
            products = products.filter(fields__price__gte=float(price_gte))
        if price_lte:
            products = products.filter(fields__price__lte=float(price_lte))
        
        # Sorting by price only (supports 'price' or '-price')
        sort_by = request.query_params.get('sort_by')
        if sort_by:
            if sort_by == 'price':
                products = products.order_by('fields__price')
            elif sort_by == '-price':
                products = products.order_by('-fields__price')
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    # Create a new product
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=201)
        return Response(serializer.errors, status=400)

# View to handle retrieving, updating, and deleting a specific product
class ProductDetailView(APIView):

    # Retrieve a product by ID
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return Response(ProductSerializer(product).data)

    # Update a product by ID
    def put(self, request, pk):
        product = Product.objects.get(pk=pk)

        # overwrite only provided keys
        product.fields.update(request.data.get("fields", {}))
        product.save()

        return Response(ProductSerializer(product).data)

    # Delete a product by ID
    def delete(self, request, pk):
        Product.objects.get(pk=pk).delete()
        return Response(status=204)
