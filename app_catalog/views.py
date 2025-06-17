from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from app_catalog.models import Dress


def dress_catalog_view(request):
    dresses = Dress.objects.all().order_by('-created_at')

    paginator = Paginator(dresses, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'app_catalog/catalog.html', context)


def dress_detail_view(request, dress_id):
    dress = get_object_or_404(Dress, pk=dress_id)
    images = dress.images.all().order_by('order')
    main_image = images.first() if images.exists() else None

    context = {
        'product': dress,
        'main_image': main_image,
        'images': images,
        'available_sizes': dress.get_sizes_list(),
    }
    return render(request, 'app_catalog/product.html', context)