import os
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from app_catalog.models import Item, ItemImage
from django.urls import reverse


class Command(BaseCommand):
    help = "Генерирует YML-фид каталога для поисковых систем"

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            default='catalog_feed.yml',
            help='Имя выходного файла (по умолчанию: catalog_feed.yml)'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        output_path = os.path.join(settings.BASE_DIR, 'static', output_file)
        
        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Функция для замены HTML-сущностей на XML-совместимые символы
        def replace_entities(text):
            if not text:
                return text
            text = text.replace('&nbsp;', ' ')
            text = text.replace('&mdash;', '—')
            text = text.replace('&ndash;', '–')
            text = text.replace('&laquo;', '«')
            text = text.replace('&raquo;', '»')
            text = text.replace('&quot;', '"')
            text = text.replace('&amp;', '&')
            return text
        
        # Базовый URL сайта
        site_url = 'https://angel-dress.ru'
        
        # Получаем все активные товары
        items = Item.objects.filter(is_active=True).prefetch_related(
            'categories', 'images', 'price_options', 'colors', 'materials', 'available_sizes'
        )
        
        # Начинаем формировать YML-файл
        with open(output_path, 'w', encoding='utf-8') as f:
            # Заголовок XML
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<!DOCTYPE yml_catalog SYSTEM "shops.dtd">\n')
            
            # Начало каталога
            current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            f.write(f'<yml_catalog date="{current_date}">\n')
            f.write('  <shop>\n')
            
            # Информация о магазине
            f.write('    <name>Angel Dress</name>\n')
            f.write('    <company>Angel Dress</company>\n')
            f.write('    <url>https://angel-dress.ru/</url>\n')
            
            # Валюта
            f.write('    <currencies>\n')
            f.write('      <currency id="RUR" rate="1"/>\n')
            f.write('    </currencies>\n')
            
            # Категории
            f.write('    <categories>\n')
            categories = {}
            category_id = 1
            
            for item in items:
                for category in item.categories.all():
                    if category.id not in categories:
                        categories[category.id] = {
                            'id': category_id,
                            'name': category.name
                        }
                        category_id += 1
            
            for category_data in categories.values():
                f.write(f'      <category id="{category_data["id"]}">{category_data["name"]}</category>\n')
            
            f.write('    </categories>\n')
            
            # Товары
            f.write('    <offers>\n')
            
            for item in items:
                # Получаем все цены для товара
                price_options = item.price_options.filter(is_active=True)
                if not price_options.exists():
                    continue  # Пропускаем товары без цены
                
                # Для совместимости берем первую цену
                first_price_option = price_options.first()
                
                # Получаем первое изображение товара
                image = item.get_first_image_url()
                if image.startswith('/'):
                    image = f"{site_url}{image}"
                
                # Формируем URL товара
                item_url = f"{site_url}{item.get_absolute_url()}"
                
                # Запись информации о товаре
                f.write(f'      <offer id="{item.id}" available="true">\n')
                f.write(f'        <url>{item_url}</url>\n')
                
                # Цена для продажи (берем из первого доступного price option)
                f.write(f'        <price>{first_price_option.price}</price>\n')
                
                # Залоговая цена
                if first_price_option.pledge:
                    f.write(f'        <deposit>{first_price_option.pledge}</deposit>\n')
                
                f.write('        <currencyId>RUR</currencyId>\n')
                
                # Артикул
                f.write(f'        <vendorCode>{item.id}</vendorCode>\n')
                
                # Категории товара
                for category in item.categories.all():
                    if category.id in categories:
                        f.write(f'        <categoryId>{categories[category.id]["id"]}</categoryId>\n')
                
                # Бренд
                if item.brand:
                    brand_name = replace_entities(item.brand.name)
                    f.write(f'        <vendor><![CDATA[{brand_name}]]></vendor>\n')
                
                # Название
                item_name = replace_entities(item.name)
                f.write(f'        <name><![CDATA[{item_name}]]></name>\n')
                
                # Размеры
                if item.available_sizes.exists():
                    sizes = ', '.join([replace_entities(size.name) for size in item.available_sizes.all()])
                    f.write(f'        <param name="Размер"><![CDATA[{sizes}]]></param>\n')
                
                # Цвет
                if item.colors.exists():
                    colors = ', '.join([replace_entities(color.name) for color in item.colors.all()])
                    f.write(f'        <param name="Цвет"><![CDATA[{colors}]]></param>\n')
                
                # Цена для аренды (берем минимальную цену аренды)
                rental_price = min([po.price for po in price_options], default=first_price_option.price)
                f.write(f'        <param name="Цена для аренды"><![CDATA[{rental_price}]]></param>\n')
                
                # Цена для продажи (уже указана как основная цена)
                f.write(f'        <param name="Цена для продажи"><![CDATA[{first_price_option.price}]]></param>\n')
                
                # Цена залога
                if first_price_option.pledge:
                    f.write(f'        <param name="Цена залога"><![CDATA[{first_price_option.pledge}]]></param>\n')
                
                f.write('      </offer>\n')
            
            # Закрываем теги
            f.write('    </offers>\n')
            f.write('  </shop>\n')
            f.write('</yml_catalog>')
        
        self.stdout.write(self.style.SUCCESS(f'YML-фид успешно сгенерирован: {output_path}'))
