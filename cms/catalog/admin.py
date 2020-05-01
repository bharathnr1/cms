from django.contrib import admin
from .models import Product, Images, Category, SubCategory, Cart
# Register your models here.
admin.site.register(Product)
admin.site.register(Images)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Cart)
