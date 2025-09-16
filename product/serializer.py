from rest_framework import serializers
from django.db.models import Avg, Count
from .models import Product, Category, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'stars')


class ProductDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField(read_only=True) 
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'category', 'reviews')


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'category')
        
        
class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'reviews', 'rating')

    def get_rating(self, product):
        return product.reviews.aggregate(avg_stars=Avg('stars')).get('avg_stars') or 0



class CategoryWithProductCountSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'products_count')

    def get_products_count(self, category):
        return category.products.count()
    
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'category')
        
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'stars', 'product')