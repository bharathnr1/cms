from django.contrib import admin
from .models import Product, ProductAdmin, Images, Category, SubCategory, Cart, Dimension, PrimaryMaterial, Vendor
# Register your models here.


admin.site.register(Product, ProductAdmin)
admin.site.register(Images)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Cart)
admin.site.register(Dimension)
admin.site.register(PrimaryMaterial)
admin.site.register(Vendor)
