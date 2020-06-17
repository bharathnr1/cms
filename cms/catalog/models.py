from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib import admin
from multiselectfield import MultiSelectField


# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=30)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
            self.slug = self.slug or slugify(self.category)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.category

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=30)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
            self.slug = self.slug or slugify(self.sub_category)
            super().save(*args, **kwargs)
            
    def __str__(self):
        return self.sub_category



VENDOR_TYPE_CHOICES = [
    ('Manufacturer', 'Manufacturer'),
    ('Trader', 'Trader'),
    ('Shop', 'Shop'),
]
QUALITY_STANDARDS_CHOICES = [
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low')
]
SCALE_OF_COMPANY_CHOICES = [
    ('Very Big', 'Very Big'),
    ('Big', 'Big'),
    ('Medium', 'Medium'),
    ('Small', 'Small'),
    ('Very Small', 'Very Small')
]
PREVIOUS_EXP_CHOICES = [
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low')
]
CUSTOMIZATION_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No')
]
RATING_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]


class Vendor(models.Model):
    company_name = models.CharField(max_length=40, blank=False, null=False)
    vendor_type = models.CharField(max_length=15, blank=False, null=False, choices=VENDOR_TYPE_CHOICES)
    contact_name = models.CharField(max_length=40, blank=False, null=False)
    wechat = models.IntegerField(blank=False, null=False)
    contact_no = models.IntegerField(blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    address_street = models.CharField(max_length=80, blank=True, null=True)
    address_city = models.CharField(max_length=30, blank=True, null=True)
    address_province = models.CharField(max_length=30, blank=True, null=True)
    address_country = models.CharField(max_length=20, blank=True, null=True)
    quality_standards = models.CharField(max_length=10, blank=True, null=True, choices=QUALITY_STANDARDS_CHOICES)
    previous_exp = models.CharField(max_length=10, blank=True, null=True, choices=PREVIOUS_EXP_CHOICES)
    business_till_date = models.CharField(max_length=80, blank=True, null=True)
    commitment_level = models.IntegerField(blank=True, null=True)
    customization = models.CharField(max_length=5, blank=True, null=True, choices=CUSTOMIZATION_CHOICES)
    payment_terms = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=10, blank=True, null=True, choices=RATING_CHOICES)
    observations = models.CharField(max_length=100, blank=False)

    # category field which shows core category/product the vendor is specialized in - this can be more than one.

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
            self.slug = self.slug or slugify(self.company_name)
            super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=30, blank=False)
    vendor_model_no = models.CharField(max_length=30, blank=False, default='v123')
    model_no = models.CharField(max_length=30, blank=False, default='hstc123')
    finish = models.CharField(max_length=30, blank=False, default='finish')
    color = models.CharField(max_length=30, blank=False)
    weight = models.CharField(max_length=30, blank=False)
    
    unit = models.CharField(max_length=30, blank=False, default='unit')
    packing = models.CharField(max_length=30, blank=False, default='packing')
    cbm = models.IntegerField(blank=False, default=0)

    min_price = models.IntegerField(blank=False, default=10)
    max_price = models.IntegerField(blank=False, default=100000)

    moq = models.IntegerField(blank=False, default=0)
    lead_time = models.IntegerField(blank=False, default=0)
    remarks = models.CharField(max_length=100, blank=False, default='remarks')

    # Foreign Key fields
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ManyToManyField(SubCategory)

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


class Dimension(models.Model):
    d_field_name = models.CharField(max_length=20, blank=True, null=True)
    d_field_value = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

class PrimaryMaterial(models.Model):
    m_field_name = models.CharField(max_length=30, blank=True, null=True)
    m_field_value = models.CharField(max_length=30, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    readonly_fields = ('id',)


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

    