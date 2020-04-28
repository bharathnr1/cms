import django_filters

from .models import Product

class ProductFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='icontains')
    # color = django_filters.CharFilter(lookup_expr='iexact')
    # model = django_filters.CharFilter(lookup_expr='iexact')

    # length__gt = django_filters.NumberFilter(name='length', lookup_expr='length__gt')
    # width__gt = django_filters.NumberFilter(name='width', lookup_expr='width__gt')
    # height__gt = django_filters.NumberFilter(name='height', lookup_expr='height__gt')
    # length__lt = django_filters.NumberFilter(name='length', lookup_expr='length__lt')
    # width__lt = django_filters.NumberFilter(name='width', lookup_expr='width__lt')
    # height__t = django_filters.NumberFilter(name='height', lookup_expr='height__lt')

    # category = django_filters.CharFilter(lookup_expr='iexact')
    # sub_category = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Product
        fields = '__all__'