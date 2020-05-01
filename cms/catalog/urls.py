from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [

    #Approve Staff Accounts
    path('approve_staff', views.approve_staff, name='approve_staff'),

    #Display Pages
    path('', views.products_display, name='products_display'),
    path('prod_display/<slug:slug>', views.prod_display, name='prod_display'),
    path('categories_display', views.categories_display, name='categories_display'),
    path('sub_categories_display', views.sub_categories_display, name='sub_categories_display'),


    # Add stuff
    path('product_add/', views.product_add, name='product_add'),
    path('category_add/', views.category_add, name='category_add'),
    path('sub_category_add/', views.sub_category_add, name='sub_category_add'),

    # dummy redirect to calculate sub-categories based on categories
    path('ajax/load_sub_categories/', views.load_sub_categories, name='load_sub_categories'),  

    # Search
    path('search/', views.search, name='search'),

    # Cart
    path('cart_display/', views.cart_display, name='cart_display'),
    
    # PDF Creation from cart
    path('generate_pdf_cart/', views.generate_pdf_cart, name='generate_pdf_cart')

]
