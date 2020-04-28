from django.shortcuts import render
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ImageForm, ProductForm, CategoryForm, SubCategoryForm
from .models import Product, Images, Category, SubCategory
from .filters import ProductFilter

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse


# Create your views here.

# def catalog(request):
#     return render(request, 'catalog.html')

# Add a product
def product_add(request):

    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm, extra=6)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':

        productForm = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())


        if productForm.is_valid() and formset.is_valid():
            product_form = productForm.save()
            
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(product=product_form, image=image)
                    photo.save()
            return HttpResponseRedirect(reverse('catalog:products_display'))
            # return render(request, 'products_display.html')
        else:
            print(productForm.errors, formset.errors)
    else:
        productForm = ProductForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'product_add.html',
                  {'productForm': productForm, 'formset': formset})

# View all the products
def products_display(request):
    products = Product.objects.all()
    # print(products[1].pk)
    return render(request, 'products_display.html', {'products': products})


# View each product
def prod_display(request, slug):
    print(slug)
    prod = get_object_or_404(Product, slug=slug)
    return render(request, 'prod_display.html', {'prod': prod})

# Return Sub-Categories for each category
def load_sub_categories(request):
    print(request.GET.get('category'))
    category_id = request.GET.get('category')
    sub_categories = SubCategory.objects.filter(category_id=category_id).order_by('sub_category')
    return render(request, 'load_sub_categories.html', {'sub_categories': sub_categories})

# Add a new Category
def category_add(request):
    categoryform = CategoryForm()
    if request.method == 'POST':
        categoryform = CategoryForm(request.POST)
        print(categoryform.errors)
        categoryform.save()
        return HttpResponseRedirect(reverse('catalog:products_display'))
    return render(request, 'category_add.html', {'categoryform': categoryform})

# Add a new Sub-Category
def sub_category_add(request):
    subcategoryform = SubCategoryForm()
    if request.method == 'POST':
        subcategoryform = SubCategoryForm(request.POST)
        print(subcategoryform.errors)
        subcategoryform.save()
        return HttpResponseRedirect(reverse('catalog:products_display'))
    return render(request, 'sub_category_add.html', {'subcategoryform': subcategoryform})


# Search
def search(request):
	products = Product.objects.all()
	product_filter = ProductFilter(request.GET, queryset = products)
	return render(request, 'search.html', {'product_filter' : product_filter})
