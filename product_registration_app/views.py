from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 100


class ProductRegistrationView(generics.CreateAPIView):
    """
        API endpoint for registering a new product.

        Request Method: POST

        Parameters:
        - name (str): Name of the product.
        - description (str): Description of the product.
        - manufacturer (str): Manufacturer of the product.
        - serial_number (str): Serial number of the product.
        - date_of_manufacture (str): Date of manufacture of the product in the format 'YYYY-MM-DD'.
        - warranty_information (str): Warranty information of the product.
        - category (str): Category of the product.

        Returns:
        - If successful, returns the details of the registered product with status code 201 (Created).
        - If validation fails, returns error messages with status code 400 (Bad Request).
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            error_messages = []
            for field, messages in errors.items():
                for message in messages:
                    error_messages.append(f"{field}: {message}")
            return Response({"errors": error_messages}, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    """
        API endpoint for listing products.

        Request Method: GET

        Parameters:
        - name (str, optional): Filter products by name.
        - manufacturer (str, optional): Filter products by manufacturer.
        - category (str, optional): Filter products by category.

        Returns:
        - Returns a paginated list of products based on the provided filters.
    """

    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'manufacturer', 'category']
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        name = self.request.query_params.get('name')
        manufacturer = self.request.query_params.get('manufacturer')
        category = self.request.query_params.get('category')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if manufacturer:
            queryset = queryset.filter(manufacturer__icontains=manufacturer)
        if category:
            queryset = queryset.filter(category__icontains=category)
        return queryset


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
        API endpoint for retrieving, updating, and deleting a product.

        Request Methods:
        - GET: Retrieve details of a product by its ID.
        - PUT/PATCH: Update details of a product by its ID.
        - DELETE: Delete a product by its ID.

        Returns:
        - If successful, returns the details of the product with status code 200 (OK).
        - If validation fails during update, returns error messages with status code 400 (Bad Request).
        - If the product is successfully deleted, returns a success message with status code 204 (No Content).
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if not self.validate_update_data(serializer.validated_data):
            return Response({'message': 'Validation failed'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Product Deleted'}, status=status.HTTP_204_NO_CONTENT)

    def validate_update_data(self, validated_data):
        if 'manufacturer' in validated_data or 'date_of_manufacture' in validated_data:
            return False
        return True
