from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Promotion


def promotions_list(request):
    promotions_list = Promotion.objects.filter(
        is_active=True,
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()
    ).order_by('order')

    paginator = Paginator(promotions_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': 'Акции',
        'meta_description': 'Специальные предложения и акции от Angel Dress. Узнайте о текущих скидках и выгодных условиях.'
    }
    return render(request, 'app_promotion/promotions_list.html', context)


def promotion_detail(request, promotion_id):
    promotion = get_object_or_404(
        Promotion,
        id=promotion_id,
        is_active=True,
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()
    )

    context = {
        'promotion': promotion,
        'title': promotion.title
    }
    return render(request, 'app_promotion/promotion_detail.html', context)
