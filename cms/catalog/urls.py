from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [

    #Catalog Pages
    path('', views.products_display, name='products_display'),
    path('prod_display/<slug:slug>', views.prod_display, name='prod_display'),

    # Add stuff
    path('product_add/', views.product_add, name='product_add'),
    path('category_add/', views.category_add, name='category_add'),
    path('sub_category_add/', views.sub_category_add, name='sub_category_add'),

    # dummy redirect to calculate sub-categories based on categories
    path('ajax/load_sub_categories/', views.load_sub_categories, name='load_sub_categories'),  

    # Search
    path('search/', views.search, name='search'),
    
]
