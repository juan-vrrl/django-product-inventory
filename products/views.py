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
        name = request.query_params.get("name")
        if name:
            products = products.filter(fields__name__icontains=name)

        # Filter by price range
        price_gte = request.query_params.get("price_gte")  # greater than or equal
        price_lte = request.query_params.get("price_lte")  # less than or equal

        if price_gte:
            products = products.filter(fields__price__gte=float(price_gte))
        if price_lte:
            products = products.filter(fields__price__lte=float(price_lte))

        # Order by price (supports 'asc' for ascending or 'desc' for descending)
        order = request.query_params.get("order")
        if order:
            if order == "asc":
                products = products.order_by("fields__price")
            elif order == "desc":
                products = products.order_by("-fields__price")

        # Pagination
        page = int(request.query_params.get("page", 1))
        limit = int(request.query_params.get("limit", 10))

        # Calculate offset
        offset = (page - 1) * limit

        # Get total count before pagination
        total_count = products.count()

        # Apply pagination
        products = products[offset : offset + limit]

        serializer = ProductSerializer(products, many=True)
        return Response(
            {
                "status": 200,
                "message": "Products retrieved successfully",
                "metadata": {
                    "page": page,
                    "limit": limit,
                    "total": total_count,
                    "total_pages": (total_count + limit - 1) // limit,
                },
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # Create a new product
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(
                {
                    "status": 201,
                    "message": "Product created successfully",
                    "data": ProductSerializer(product).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": 400,
                "message": "Failed to create product",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# View to handle retrieving, updating, and deleting a specific product
class ProductDetailView(APIView):

    # Retrieve a product by ID
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return Response(
            {
                "status": 200,
                "message": "Product retrieved successfully",
                "data": ProductSerializer(product).data,
            },
            status=status.HTTP_200_OK,
        )

    # Update a product by ID
    def put(self, request, pk):
        product = Product.objects.get(pk=pk)

        # overwrite only provided keys
        product.fields.update(request.data.get("fields", {}))
        product.save()

        return Response(
            {
                "status": 200,
                "message": "Product updated successfully",
                "data": ProductSerializer(product).data,
            },
            status=status.HTTP_200_OK,
        )

    # Delete a product by ID
    def delete(self, request, pk):
        Product.objects.get(pk=pk).delete()
        return Response(
            {"status": 204, "message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
