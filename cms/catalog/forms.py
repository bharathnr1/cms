from django import forms
from .models import Product, Images, Category, SubCategory, Cart, Dimension, PrimaryMaterial, Vendor

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
                "name",
                "vendor_model_no",
                "model_no",
                "finish",
                "color",
                "weight",
                "unit",
                "packing",
                "cbm",
                "min_price",
                "max_price",
                "moq",
                "lead_time",
                "remarks",
                "category",
                "sub_category",
                )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_category'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('sub_category')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty sub_category queryset
        elif self.instance.pk:
            self.fields['sub_category'].queryset = self.instance.category.sub_category_set.order_by('sub_category')

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Images
        fields = ('image', )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category',)

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ('sub_category', 'category')


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ()

class DimensionForm(forms.ModelForm):
    d_field_name = forms.CharField(label='dimension')
    class Meta:
        model = Dimension
        fields = ('d_field_name','d_field_value')
    
    # category = forms.ModelChoiceField(queryset=Dimension.objects.none())
    # product = forms.ModelChoiceField(queryset=Product.objects.none())    

class PrimaryMaterialForm(forms.ModelForm):
    m_field_name = forms.CharField(label='primary_material')
    class Meta:
        model = PrimaryMaterial
        fields = ('m_field_name','m_field_value')

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'
