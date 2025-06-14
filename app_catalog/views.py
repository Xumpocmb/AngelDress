from django.shortcuts import render

def catalog_view(request):
    return render(request, 'app_catalog/catalog.html')


def product_view(request):
    return render(request, 'app_catalog/product.html')