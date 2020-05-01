from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ImageForm, ProductForm, CategoryForm, SubCategoryForm, CartForm
from accounts.forms import SignupCustomerForm
from .models import Product, Images, Category, SubCategory, Cart
from accounts.models import SignupCustomer
from .filters import ProductFilter

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
import os

#PDF Modules
from io import BytesIO
from xhtml2pdf import pisa   
from django.template.loader import get_template 
from django.core.files.base import ContentFile

# Create your views here.

# Approve staff account
def approve_staff(request):
    pending_approvals = SignupCustomer.objects.filter(approved=False)
    print(pending_approvals)
    # staff_form = SignupCustomerForm()
    if request.method == 'POST':
        staff_form = SignupCustomerForm(request.POST)
        if 'approve' in request.POST:
            if 'user' in request.POST:
                user_id = request.POST.get('user') 
                print(request.POST.get('user'))
            print("Approve Button")
            staff = SignupCustomer.objects.get(user_id=user_id)
            staff.approved = True
            staff.user.is_active = True
            staff.save()
            staff.user.save()
            return redirect(reverse('catalog:approve_staff'))
                
        if 'reject' in request.POST:
            if 'user' in request.POST:
                user_id = request.POST.get('user') 
                print(request.POST.get('user'))
            print("Reject Button")
            SignupCustomer.objects.get(user_id=user_id).delete()
            return HttpResponseRedirect(reverse('catalog:approve_staff')) 
    return render(request, 'approve_staff.html', {'pending_approvals': pending_approvals})
    

# Add a product
@login_required
def product_add(request):
    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm, extra=10)
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
@user_passes_test(lambda u: u.is_superuser)
def products_display(request):
    products = Product.objects.all()
    addtocartForm = CartForm(request.POST)
    # print(products[1].pk)
    return render(request, 'products_display.html', {'products': products, 'addtocartForm': addtocartForm})

# View all categories
def categories_display(request):
    categories = Category.objects.all()
    return render(request, 'categories_display.html', {'categories': categories})

# View all sub-categories
def sub_categories_display(request):
    sub_categories = SubCategory.objects.all()
    return render(request, 'sub_categories_display.html', {'sub_categories': sub_categories})


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

# Cart 
def cart_display(request):
    cart = Cart.objects.filter(user=request.user).order_by('product__category')
    # print(cart)
    category_list = Category.objects.values_list('category', flat=True).distinct()
    # print(category_list)
    cart_by_category = {}
    for cat in category_list:
        if Cart.objects.filter(user=request.user, product__category__category=cat):
            cart_by_category[cat] = Cart.objects.filter(user=request.user, product__category__category=cat)
    print(cart_by_category)

    if request.method == 'POST':
        addtocartForm = CartForm(request.POST)
        if 'addtocart' in request.POST:
            if 'product' in request.POST:
                product_id = request.POST.get('product') 
                #print(request.POST.get('product'))
            print("Add to Cart")
            current_product = Product.objects.get(id=product_id)
            current_user = request.user
            # print(current_user)
            # print(current_product)
            Cart.objects.create(user=current_user, product=current_product)
            return redirect(reverse('catalog:products_display'))
                
        if 'removefromcart' in request.POST:
            if 'product' in request.POST:
                product_id = request.POST.get('product') 
                print(request.POST.get('user'))
            print("Remove from Cart")
            current_product = Product.objects.get(id=product_id)
            current_user = request.user
            Cart.objects.filter(product=current_product).delete()
            return HttpResponseRedirect(reverse('catalog:products_display'))

    return render(request, 'cart_display.html', {'cart': cart, 'cart_by_category': cart_by_category})


# Converting Carts to pdfs
"""
Use to convert the image url to absolute URL 

"""
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources

    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path         
"""

1. We need to check while creating the Shipment marks how to lower down the resolution of the images that are being attachec
2. We need to create seprate button to send email to customer

"""

def generate_pdf_cart(request):
    category_list = Category.objects.values_list('category', flat=True).distinct()
    # print(category_list)
    cart_by_category = {}
    for cat in category_list:
        if Cart.objects.filter(user=request.user, product__category__category=cat):
            cart_by_category[cat] = Cart.objects.filter(user=request.user, product__category__category=cat)
    print(cart_by_category)
    # customer_object = get_object_or_404(Customer, pk=pk)
    # vendor_obj = Customer_Details.objects.filter(customer=customer_object).all()    
    data = {"cart_by_category":cart_by_category}
    template = get_template("cart_pdf.html")
    html = template.render(data)
    response = BytesIO()
    x=str(settings.MEDIA_ROOT).replace("\\","/")
    x=x+"/mypdf.pdf"
    output = open(x, 'wb+')
    pdfPage = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    output.write(response.getvalue())
    output.close()
  
    # email = EmailMessage(
    #         'Hello',
    #         'Body goes here',
    #         settings.EMAIL_HOST_USER,
    #         ["asisbagga@gmail.com"],
    #         ['asissingh.g@gmail.com'],
    #         headers={'Message-ID': 'foo'},)
    # email.attach_file(x)
    # email.send()

    os.remove(x)
    if not pdfPage.err:
       return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Oops got an Error, Try again!")
