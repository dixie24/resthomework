from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Category
from .serializer import ProductListSerializer, ProductDetailSerializer, ProductWithReviewsSerializer, CategoryWithProductCountSerializer


@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = ProductListSerializer(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)




@api_view(['GET'])
def product_detail_api_view(request,id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Product not found!'})
    
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