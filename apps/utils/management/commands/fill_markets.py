# Vendor
import json
from itertools import product

from django.conf import settings
from django.core.management.base import BaseCommand

# Local
from apps.product import models as product_models
from apps.market import models as market_models


class Command(BaseCommand):
    help = "Autofill products and markets from geojson"

    def handle(self, *args, **options):
        # Создаем продукты
        print("check products")


        latin_to_kirill = {
            'khleb': 'Хлеб',
            'muka': 'Мука',
            'rozhki': 'Рожки',
            'krupa_grechnevaya': 'Гречневая крупа',
            'rice_shlifovanniy': 'Шлифованный рис',
            'kartofel': 'Картофель',
            'morkov': 'Морковь',
            'luk_repchatiy': 'Репчатый лук',
            'kapusta': 'Капуста',
            'sahar': 'Сахар',
            'maslo_podsolnechnoie': 'Подсолнечное масло',
            'govyadina': 'Говядина',
            'myaso_kur': 'Куриное мясо',
            'moloko_pasterizovannoie': 'Пастеризованное молоко',
            'kefir': 'Кефир',
            'maslo_slivochnoie': 'Сливочное масло',
            'yaitso': 'Яйцо',
            'sol_povarennaya': 'Поваренная соль',
            'tvorog': 'Творог'
        }


        with open(f'{settings.BASE_DIR}/help_files/markets_and_products.geojson', encoding='utf-8') as f:
            products_json = json.load(f)

        print("start to add products:\n")

        products_added = False
        for count, item in enumerate(products_json['features']):
            longitude, latitude = item['geometry']['coordinates']
            coordinates = {'latitude': latitude, 'longitude': longitude}
            address = item['properties']['address']

            if not products_added:
                for name in item['properties']:
                    name_ru = latin_to_kirill.get(name)
                    price = item['properties'][name]
                    market_name = item['properties']['name']

                    if name_ru:
                        if not price:
                            price = 1000

                        product_models.Product.objects.filter(name_ru=name_ru).update_or_create(name_ru=name_ru,
                                                                                                defaults={'price': price})
                        print('--->', name_ru, price)
                        products_added = True


            print('market_name', market_name)
            print('address', address)
            print('coordinates', coordinates)

            market_name = item['properties']['name']

            market_models.Market.objects.filter(coordinates=coordinates).update_or_create(name_ru=market_name, defaults={
                'address': address,
                'coordinates': coordinates})

            print(f"{market_name} added/updated\n")
