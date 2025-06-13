from django.shortcuts import render

def catalog_view(request):
    return render(request, 'app_catalog/catalog.html')