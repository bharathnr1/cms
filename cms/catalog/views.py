from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.conf import settings


# Forms import
from .forms import ImageForm, ProductForm, ProductForm_1, ProductForm_2, CategoryForm, SubCategoryForm, CartForm, DimensionForm, PrimaryMaterialForm, VendorForm
from accounts.forms import SignupCustomerForm
from django.forms import modelformset_factory


# Models Import
from .models import Product, Images, Category, SubCategory, Cart, Dimension, PrimaryMaterial, Vendor
from accounts.models import SignupCustomer
from .filters import ProductFilter

import os

#PDF Modules
from io import BytesIO
from xhtml2pdf import pisa   
from django.template.loader import get_template 
from django.core.files.base import ContentFile

# Emails
from django.core.mail import send_mail


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
        print(request.POST)
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
            
            # Capture Dimension field values from request.post and save it in Dimension Model 
            if request.POST.get('form-0-d_field_name'):
                d_field_name = request.POST.get('form-0-d_field_name')
                d_field_value = request.POST.get('form-0-d_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                dimension = Dimension(category=category, product=product_form, d_field_name=d_field_name, d_field_value=d_field_value)
                dimension.save()
            if request.POST.get('form-1-d_field_name'):
                d_field_name = request.POST.get('form-1-d_field_name')
                d_field_value = request.POST.get('form-1-d_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                dimension = Dimension(category=category, product=product_form, d_field_name=d_field_name, d_field_value=d_field_value)
                dimension.save()
            if request.POST.get('form-2-d_field_name'):
                d_field_name = request.POST.get('form-2-d_field_name')
                d_field_value = request.POST.get('form-2-d_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                dimension = Dimension(category=category, product=product_form, d_field_name=d_field_name, d_field_value=d_field_value)
                dimension.save()
            if request.POST.get('form-3-d_field_name'):
                d_field_name = request.POST.get('form-3-d_field_name')
                d_field_value = request.POST.get('form-3-d_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                dimension = Dimension(category=category, product=product_form, d_field_name=d_field_name, d_field_value=d_field_value)
                dimension.save()
            if request.POST.get('form-4-d_field_name'):
                d_field_name = request.POST.get('form-4-d_field_name')
                d_field_value = request.POST.get('form-4-d_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                dimension = Dimension(category=category, product=product_form, d_field_name=d_field_name, d_field_value=d_field_value)
                dimension.save()
            if request.POST.get('form-5-d_field_name'):
                d_field_name = request.POST.get('form-5-d_field_name')
                d_field_value = request.POST.get('form-5-d_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                dimension = Dimension(category=category, product=product_form, d_field_name=d_field_name, d_field_value=d_field_value)
                dimension.save()
            
             # Capture Primary Material field values from request.post and save it in Primary Material Model 
            if request.POST.get('form-0-m_field_name'):
                m_field_name = request.POST.get('form-0-m_field_name')
                m_field_value = request.POST.get('form-0-m_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                pm = PrimaryMaterial(category=category, product=product_form, m_field_name=m_field_name, m_field_value=m_field_value)
                pm.save()
            if request.POST.get('form-1-m_field_name'):
                m_field_name = request.POST.get('form-1-m_field_name')
                m_field_value = request.POST.get('form-1-m_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                pm = PrimaryMaterial(category=category, product=product_form, m_field_name=m_field_name, m_field_value=m_field_value)
                pm.save()
            if request.POST.get('form-2-m_field_name'):
                m_field_name = request.POST.get('form-2-m_field_name')
                m_field_value = request.POST.get('form-2-m_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                pm = PrimaryMaterial(category=category, product=product_form, m_field_name=m_field_name, m_field_value=m_field_value)
                pm.save()
            if request.POST.get('form-3-m_field_name'):
                m_field_name = request.POST.get('form-3-m_field_name')
                m_field_value = request.POST.get('form-3-m_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                pm = PrimaryMaterial(category=category, product=product_form, m_field_name=m_field_name, m_field_value=m_field_value)
                pm.save()
            if request.POST.get('form-4-m_field_name'):
                m_field_name = request.POST.get('form-4-m_field_name')
                m_field_value = request.POST.get('form-4-m_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                pm = PrimaryMaterial(category=category, product=product_form, m_field_name=m_field_name, m_field_value=m_field_value)
                pm.save()
            if request.POST.get('form-5-m_field_name'):
                m_field_name = request.POST.get('form-5-m_field_name')
                m_field_value = request.POST.get('form-5-m_field_value')
                category_id = request.POST.get('category')
                category = get_object_or_404(Category, id=category_id)
                pm = PrimaryMaterial(category=category, product=product_form, m_field_name=m_field_name, m_field_value=m_field_value)
                pm.save()

            return HttpResponseRedirect(reverse('catalog:products_display'))
        else:
            print(productForm.errors, formset.errors)
    else:
        productForm = ProductForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'product_add.html',
                  {'productForm': productForm, 
                   'formset': formset,
                  })

# View all the products
@user_passes_test(lambda u: u.is_superuser)
def products_display(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    dict={}
    for category in categories:
        subcategories = SubCategory.objects.filter(category=category)
        for sub_cat in subcategories:
                if category in dict:
                    dict[category].append(sub_cat)
                else:
                    dict[category]=[sub_cat]
    addtocartForm = CartForm(request.POST)
    # print(products[1].pk)
    return render(request, 'products_display.html', {'products': products, 'addtocartForm': addtocartForm, 'cat_list':dict})

def product_list(request, cat, sc):
    products = Product.objects.filter(sub_category=sc)
    return render(request, 'products_list.html', {'products':products})

# View all categories
def categories_display(request):
    categories = Category.objects.all()
    return render(request, 'categories_display.html', {'categories': categories})

# def category_display(request, slug):
#     category = Category.objects.get(slug=slug)
#     if request.method == 'POST':
#         dimensionform = DimensionForm(request.POST)
#         primarymaterialform = PrimaryMaterialForm(request.POST)
#         if dimensionform.is_valid() and primarymaterialform.is_valid():
#             dform = dimensionform.save(commit=False)
#             dform.category = category.pk
#             dform.save()
#             pmform = primarymaterialform.save(commit=False)
#             pmform.category = category.pk
#             pmform.save()
#         else:
#             print(dimensionform.errors)
#             print(primarymaterialform.errors)
#     else:
#         dimensionform = DimensionForm()
#         primarymaterialform = PrimaryMaterialForm()
#     return render(request, 'category_display.html', {'category': category, 'dimensionform': dimensionform, 'primarymaterialform': primarymaterialform})

# View all sub-categories
def sub_categories_display(request):
    sub_categories = SubCategory.objects.all()
    return render(request, 'sub_categories_display.html', {'sub_categories': sub_categories})

def sub_category_display(request, slug):
    sub_category = SubCategory.objects.get(slug=slug)
    return render(request, 'sub_category_display.html', {'sub_category': sub_category})


# View each product
def prod_display(request, slug):
    print(slug)
    prod = get_object_or_404(Product, slug=slug)
    dimensions = Dimension.objects.filter(product=prod)
    pm = PrimaryMaterial.objects.filter(product=prod)
    return render(request, 'prod_display.html', {'prod': prod, 'dimensions': dimensions, 'pm': pm})

# Return Sub-Categories for each category
def load_sub_categories(request):
    print(request.GET.get('category'))
    category_id = request.GET.get('category')
    sub_categories = SubCategory.objects.filter(category_id=category_id).order_by('sub_category')
    return render(request, 'load_sub_categories.html', {'sub_categories': sub_categories})

# Return Dimensions for each category
def load_dimensions(request):
    print(request.GET.get('category'))
    category_id = request.GET.get('category')
    dimensions_dist = Dimension.objects.filter(category_id=category_id).values('d_field_name').distinct().count()
    dimensions = Dimension.objects.filter(category_id=category_id).order_by('category')[0:dimensions_dist]
    # print("Dimensions", dimensions)
    DimensionFormSet = modelformset_factory(Dimension,
                                        form=DimensionForm, extra=0)
    dformset = DimensionFormSet(queryset=dimensions)
    return render(request, 'load_dimensions.html', {'dformset': dformset})

# Return primary materials for each category
def load_primary_materials(request):
    print(request.GET.get('category'))
    category_id = request.GET.get('category')
    pm_dist = PrimaryMaterial.objects.filter(category_id=category_id).values('m_field_name').distinct().count()
    pm = PrimaryMaterial.objects.filter(category_id=category_id).order_by('category')[0:pm_dist]
    print("Primary material", pm)
    PrimaryMaterialFormSet = modelformset_factory(PrimaryMaterial,
                                        form=PrimaryMaterialForm, extra=0)
    mformset = PrimaryMaterialFormSet(queryset=pm)
    return render(request, 'load_primary_materials.html', {'mformset': mformset})


# Add a new Category
def category_add(request):
    DimensionFormSet = modelformset_factory(Dimension,
                                        form=DimensionForm, extra=5)
    #'extra' means the number of dimensions that you can upload   ^
    PrimaryMaterialFormSet = modelformset_factory(PrimaryMaterial,
                                        form=PrimaryMaterialForm, extra=5)
    #'extra' means the number of primary material that you can upload   ^
    if request.method == 'POST':
        categoryForm = CategoryForm(request.POST)
        formset_d = DimensionFormSet(request.POST, request.FILES,
                               queryset=Dimension.objects.none())
        formset_pm = PrimaryMaterialFormSet(request.POST, request.FILES,
                               queryset=PrimaryMaterial.objects.none())


        if categoryForm.is_valid() and formset_d.is_valid() and formset_pm.is_valid():
            print("valid")
            category_form = categoryForm.save()
            
            for form in formset_d.cleaned_data:
                # this helps to not crash if the user does not upload all the dimensions fields
                if form:
                    d_field_name = form['d_field_name']
                    dimension = Dimension(category=category_form, product=None, d_field_name=d_field_name)
                    dimension.save()
            for form in formset_pm.cleaned_data:
                # this helps to not crash if the user does not upload all the primary material fields
                if form:
                    m_field_name = form['m_field_name']
                    pm = PrimaryMaterial(category=category_form, m_field_name=m_field_name)
                    pm.save()                    
            return HttpResponseRedirect(reverse('catalog:categories_display'))
        else:
            print(formset_d.errors)
    else:
        categoryForm = CategoryForm()
        formset_d = DimensionFormSet(queryset=Dimension.objects.none())
        formset_pm = PrimaryMaterialFormSet(queryset=PrimaryMaterial.objects.none())
    return render(request, 'category_add.html',
                  {'categoryForm': categoryForm, 'formset_d': formset_d, 'formset_pm': formset_pm})


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
    addtocartForm = CartForm(request.POST)
    # product_form_first = ProductForm_1()
    # product_form_second = ProductForm_2
    return render(request, 'search.html', {'product_filter' : product_filter, "addtocartForm" : addtocartForm})

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

    addtocartForm = CartForm(request.POST)

    if request.method == 'POST':                
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
            return HttpResponseRedirect(reverse('catalog:cart_display'))
    
    return render(request, 'cart_display.html', {'cart': cart, 'cart_by_category': cart_by_category, 'addtocartForm': addtocartForm})


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

def generate_pdf_cart(request, slug):
    if slug == 'allcarts':
        category_list = Category.objects.values_list('category', flat=True).distinct()
    else:
        category_list = Category.objects.filter(category=slug).values_list('category', flat=True).distinct()
        # print(category_list)
    cart_by_category = {}
    for cat in category_list:
        if Cart.objects.filter(user=request.user, product__category__category=cat):
            cart_by_category[cat] = Cart.objects.filter(user=request.user, product__category__category=cat)
    # print(cart_by_category)
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

    os.remove(x)
    if not pdfPage.err:
       return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Oops got an Error, Try again!")


# Send email 
def send_email(request):
    email_from = settings.EMAIL_HOST_USER
    email_to = 'bharath.nr1@gmail.com'
    email_admin = settings.EMAIL_ADMIN

    content = 'Test email'

    message1 = ('Quote request', 'Have attached the pdf with the required materials', email_from, [email_to])
    message2 = ('New comedian registration', content , email_from, [email_admin])
    #send_mass_mail((message1, message2), fail_silently=False)
    send_mail(
        'Quote request',
        'Have attached the pdf containing the order.',
        email_from,
        [email_to],
        fail_silently=False,
    )
    return render(request, 'send_email.html')