from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Category, Review
from .serializer import (
    ProductListSerializer, ProductDetailSerializer, ProductWithReviewsSerializer, 
    CategoryWithProductCountSerializer, CategoryValidateSerializer, 
    ProductValidateSerializer, ReviewValidateSerializer
)


from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category, Review
from .serializer import (
    ProductListSerializer, ProductDetailSerializer, ProductWithReviewsSerializer, 
    CategoryWithProductCountSerializer, CategoryValidateSerializer, 
    ProductValidateSerializer, ReviewValidateSerializer
)


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductValidateSerializer
        return ProductListSerializer
        
    def perform_create(self, serializer):
        category_id = serializer.validated_data.pop('category')
        serializer.save(category_id=category_id)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return ProductValidateSerializer
        return ProductDetailSerializer
        
    def perform_update(self, serializer):
        category_id = serializer.validated_data.pop('category', None)
        if category_id is not None:
            serializer.save(category_id=category_id)
        else:
            serializer.save()


class ProductReviewsAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryValidateSerializer
        return CategoryWithProductCountSerializer


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryValidateSerializer
    lookup_field = 'id'


class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewValidateSerializer
        
    def perform_create(self, serializer):
        product_id = serializer.validated_data.pop('product')
        serializer.save(product_id=product_id)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewValidateSerializer
    lookup_field = 'id'
    
    def perform_update(self, serializer):
        product_id = serializer.validated_data.pop('product', None)
        if product_id is not None:
            serializer.save(product_id=product_id)
        else:
            serializer.save()

@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = ProductListSerializer(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Product not found!'})
    
    data = ProductDetailSerializer(product, many=False).data
    return Response(data=data)

@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()
    data = ProductWithReviewsSerializer(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def categories_with_count_api_view(request):
    categories = Category.objects.all()
    data = CategoryWithProductCountSerializer(categories, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST', 'PUT', 'DELETE'])
def category_cud_api_view(request, id=None):
    if request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data.get('name')
            category = Category.objects.create(name=name)
            return Response(data={'id': category.id, 'name': category.name}, status=status.HTTP_201_CREATED)

    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Category not found!'})

    if request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category.name = serializer.validated_data.get('name')
            category.save()
            return Response(data={'id': category.id, 'name': category.name}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST', 'PUT', 'DELETE'])
def product_cud_api_view(request, id=None):
    if request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            description = serializer.validated_data.get('description')
            price = serializer.validated_data.get('price')
            category_id = serializer.validated_data.get('category')
            
            product = Product.objects.create(
                title=title,
                description=description,
                price=price,
                category_id=category_id
            )
            return Response(data={'id': product.id, 'title': product.title}, status=status.HTTP_201_CREATED)

    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Product not found!'})

    if request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product.title = serializer.validated_data.get('title')
            product.description = serializer.validated_data.get('description')
            product.price = serializer.validated_data.get('price')
            product.category_id = serializer.validated_data.get('category')
            product.save()
            return Response(data={'id': product.id, 'title': product.title}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'PUT', 'DELETE'])
def review_cud_api_view(request, id=None):
    if request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            text = serializer.validated_data.get('text')
            stars = serializer.validated_data.get('stars')
            product_id = serializer.validated_data.get('product')

            review = Review.objects.create(
                text=text,
                stars=stars,
                product_id=product_id
            )
            return Response(data={'id': review.id, 'text': review.text}, status=status.HTTP_201_CREATED)

    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Review not found!'})

    if request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            review.text = serializer.validated_data.get('text')
            review.stars = serializer.validated_data.get('stars')
            review.product_id = serializer.validated_data.get('product')
            review.save()
            return Response(data={'id': review.id, 'text': review.text}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)