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
                # Получаем минимальную цену товара
                min_price_option = item.price_options.filter(is_active=True).order_by('price').first()
                if not min_price_option:
                    continue  # Пропускаем товары без цены
                
                # Получаем первое изображение товара
                image = item.get_first_image_url()
                if image.startswith('/'):
                    image = f"{site_url}{image}"
                
                # Формируем URL товара
                item_url = f"{site_url}{item.get_absolute_url()}"
                
                # Запись информации о товаре
                f.write(f'      <offer id="{item.id}" available="true">\n')
                f.write(f'        <url>{item_url}</url>\n')
                f.write(f'        <price>{min_price_option.price}</price>\n')
                
                if min_price_option.pledge:
                    f.write(f'        <oldprice>{min_price_option.pledge}</oldprice>\n')
                
                f.write('        <currencyId>RUR</currencyId>\n')
                
                # Категории товара
                for category in item.categories.all():
                    if category.id in categories:
                        f.write(f'        <categoryId>{categories[category.id]["id"]}</categoryId>\n')
                
                # Изображение
                f.write(f'        <picture>{image}</picture>\n')
                
                # Дополнительные изображения (до 10 штук)
                additional_images = item.images.all()[1:10] if item.images.count() > 1 else []
                for img in additional_images:
                    img_url = img.image.url
                    if img_url.startswith('/'):
                        img_url = f"{site_url}{img_url}"
                    f.write(f'        <picture>{img_url}</picture>\n')
                
                # Основная информация
                f.write('        <store>true</store>\n')
                f.write('        <pickup>true</pickup>\n')
                f.write('        <delivery>true</delivery>\n')
                item_name = replace_entities(item.name)
                f.write(f'        <name><![CDATA[{item_name}]]></name>\n')
                
                # Бренд (если есть)
                if item.brand:
                    brand_name = replace_entities(item.brand.name)
                    f.write(f'        <vendor><![CDATA[{brand_name}]]></vendor>\n')
                
                # Описание
                if item.description:
                    # При использовании CDATA не нужно заменять HTML-теги
                    description = item.description
                    # Заменяем неподдерживаемые HTML-сущности
                    description = replace_entities(description)
                    if len(description) > 3000:
                        description = description[:3000] + '...'
                    f.write(f'        <description><![CDATA[{description}]]></description>\n')
                
                
                # Параметры товара
                # Размеры
                if item.available_sizes.exists():
                    sizes = ', '.join([replace_entities(size.name) for size in item.available_sizes.all()])
                    f.write(f'        <param name="Размеры"><![CDATA[{sizes}]]></param>\n')
                
                # Цвета
                if item.colors.exists():
                    colors = ', '.join([replace_entities(color.name) for color in item.colors.all()])
                    f.write(f'        <param name="Цвета"><![CDATA[{colors}]]></param>\n')
                
                # Материалы
                if item.materials.exists():
                    materials = ', '.join([replace_entities(material.name) for material in item.materials.all()])
                    f.write(f'        <param name="Материалы"><![CDATA[{materials}]]></param>\n')
                
                # Характеристики платья
                if hasattr(item, 'characteristics'):
                    chars = item.characteristics
                    
                    if chars.length:
                        length_display = replace_entities(chars.get_length_display())
                        f.write(f'        <param name="Длина"><![CDATA[{length_display}]]></param>\n')
                    
                    if chars.fit:
                        fit_display = replace_entities(chars.get_fit_display())
                        f.write(f'        <param name="Фасон"><![CDATA[{fit_display}]]></param>\n')
                    
                    if chars.sleeve:
                        sleeve_display = replace_entities(chars.get_sleeve_display())
                        f.write(f'        <param name="Рукав"><![CDATA[{sleeve_display}]]></param>\n')
                    
                    if chars.train:
                        train_display = replace_entities(chars.get_train_display())
                        f.write(f'        <param name="Шлейф"><![CDATA[{train_display}]]></param>\n')
                
                # Тип застежки
                if item.fastener_type:
                    fastener_type = replace_entities(item.fastener_type.name)
                    f.write(f'        <param name="Тип застежки"><![CDATA[{fastener_type}]]></param>\n')
                
                # Детали
                if item.details:
                    details = replace_entities(item.details)
                    f.write(f'        <param name="Детали"><![CDATA[{details}]]></param>\n')
                
                # Срок аренды
                if min_price_option.rental_period_days:
                    rental_period = replace_entities(f"{min_price_option.rental_period_days} дней")
                    f.write(f'        <param name="Срок аренды"><![CDATA[{rental_period}]]></param>\n')
                
                # Тип предложения - аренда
                f.write('        <param name="Тип предложения"><![CDATA[Аренда]]></param>\n')
                
                f.write('      </offer>\n')
            
            # Закрываем теги
            f.write('    </offers>\n')
            f.write('  </shop>\n')
            f.write('</yml_catalog>')
        
        self.stdout.write(self.style.SUCCESS(f'YML-фид успешно сгенерирован: {output_path}'))