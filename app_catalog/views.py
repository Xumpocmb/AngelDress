from django.shortcuts import render

def catalog_view(request):
    return render(request, 'app_catalog/catalog.html')


def product_view(request):
    product = {
        'id': 1,
        'name': 'Платье пудрово-розовое',
        'price': '8 700 - 14 500 ₽',
        'description': 'Элегантное платье для особых случаев...',
    }

    available_sizes = ['XS', 'S', 'M', 'L', 'XL']

    additional_info = {
        'material_composition': '95% полиэстер, 5% эластан',
        'care_instructions': 'Ручная стирка при 30°C...',
        'delivery_info': 'Доставка 2-5 дней по Москве...',
        'return_policy': 'Возврат в течение 14 дней...',
    }

    context = {
        'product': product,
        'available_sizes': available_sizes,
        'additional_info': additional_info,
    }
    return render(request, 'app_catalog/product.html', context)