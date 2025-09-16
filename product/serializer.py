from rest_framework import serializers
from django.db.models import Avg, Count
from .models import Product, Category, Review, STARS

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
        
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Имя категории не может быть пустым.")
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Категория уже существует.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'category')
        
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительным")
        return value
    
    def validate_category(self, value):
        if not Category.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Указанная категория не существует.")
        return value

        
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'stars', 'product')

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Текст отзыва не может быть пустым.")
        return value

    def validate_stars(self, value):
        valid_stars = [choice[0] for choice in STARS]
        if value not in valid_stars:
            raise serializers.ValidationError("Количество звёзд должно быть от 1 до 5.")
        return value
    
    def validate_product(self, value):
        if not Product.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Указанный товар не существует.")
        return value