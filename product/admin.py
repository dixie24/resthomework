from django.contrib import admin
from .models import Category, Product, Review
# Register your models here.

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)