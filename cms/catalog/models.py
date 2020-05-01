from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=30)

    def __str__(self):
        return self.sub_category


class Product(models.Model):
    name = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=130, blank=True)
    color = models.CharField(max_length=30, blank=False)
    weight = models.CharField(max_length=30, blank=False)
    model = models.CharField(max_length=30, blank=False)
    primary_material = models.CharField(max_length=30, blank=False)
    finish = models.CharField(max_length=30, blank=False)
    length = models.DecimalField(max_digits=6, decimal_places=3, blank=False)
    width = models.DecimalField(max_digits=6, decimal_places=3, blank=False)
    height = models.DecimalField(max_digits=6, decimal_places=3, blank=False)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
            self.slug = self.slug or slugify(self.name)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

def get_image_filename(instance, filename):
    title = instance.product.name
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename) 


class Images(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')


# Cart System
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    
    def __str__(self):
        return str(self.product)

    