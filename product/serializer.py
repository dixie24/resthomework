from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
    
 
class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=1, max_length=100)

    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Имя категории не может быть пустым.")
        if Category.objects.filter(name=value).exists():
            raise ValidationError("Категория с таким именем уже существует.")
        return value

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=200)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    category = serializers.IntegerField(required=True) 

    def validate_category(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError("Указанная категория не существует.")
        return category_id

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=1)
    stars = serializers.IntegerField(required=True, min_value=1, max_value=5)
    product = serializers.IntegerField(required=True) # Имя поля 'product'

    def validate_product(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Указанный товар не существует.")
        return product_id