from django import forms
from .models import Product, Images, Category, SubCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
                "name",
                "description",
                "color",
                "weight",
                "model",
                "primary_material",
                "finish",
                "length",
                "width",
                "height",
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

  