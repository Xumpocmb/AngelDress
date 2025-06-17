import random

from django.shortcuts import render

from app_catalog.models import Dress
from app_home.models import SliderImage, ContactInfo


def index_view(request):
    slider_images = SliderImage.objects.all().order_by('order')

    # Получаем 6 случайных платьев
    random_dresses = Dress.objects.prefetch_related('images').order_by('?')[:6]

    context = {
        'slider_images': slider_images,
        'random_dresses': random_dresses,
    }
    return render(request, 'app_home/index.html', context=context)


def contact_view(request):
    return render(request, 'app_home/contacts.html')


def about_view(request):
    return render(request, 'app_home/about.html')