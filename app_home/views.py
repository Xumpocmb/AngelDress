from django.shortcuts import render

from app_home.models import SliderImage, ContactInfo


def index_view(request):
    slider_images = SliderImage.objects.all().order_by('order')
    context = {
        'slider_images': slider_images,
    }
    return render(request, 'app_home/index.html', context=context)


def contact_view(request):
    return render(request, 'app_home/contacts.html')


def about_view(request):
    return render(request, 'app_home/about.html')