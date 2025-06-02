# Vendor
import json
from django.core.management.base import BaseCommand
from django.conf import settings

# Local
from apps.utils import models as utils_models
from apps.utils.models import RegionTypeChoice


class Command(BaseCommand):
    help = "Autofill regions from json"

    def handle(self, *args, **options):
        # Создаем страну
        print("check country Kazakhstan")

        default_cities = [
            'Астана'
        ]
        popular_cities = [
            'Астана',
            'Шымкент',
            'Алматы'
        ]
        main_cities = [
            'Астана',
            'Шымкент',
            'Алматы'
        ]
        country_data = {
            'name_ru': 'Казахстан',
            'name_kk': 'Қазақстан',
            'code': 'kz'
        }
        country_obj = utils_models.Country.objects.filter(
            code=country_data['code']
        ).last()

        if not country_obj:
            country_obj = utils_models.Country.objects.create(**country_data)
            country_obj.save()
            print("country Kazakhstan created")
        print(f"country is checked, country_id={country_obj.id}\n__________")

        with open(f'{settings.BASE_DIR}/help_files/kz_regions_cities_coordinates.json', encoding='utf-8') as f:
            regions_json = json.load(f)

        print("start to add regions and ctites:\n")
        for count, region in enumerate(regions_json):
            is_default = False
            is_popular = False
            is_main = False

            code = region['code']
            ru = region['ru']
            kk = region['kk']
            region_type = region['type']
            coordinates = region['coordinates']
            parent_ru = region.get('parent', '')
            centroid = region.get('centroid', '')

            print(f"#{count + 1}. {ru} - {parent_ru}")

            if ru in default_cities:
                is_default = True
            if ru in popular_cities:
                is_popular = True
            if ru in main_cities:
                is_main = True

            parent_obj = utils_models.Region.objects.filter(name_ru=parent_ru).exclude(
                region_type=RegionTypeChoice.DISTRICT).last()

            defaults = {'name_ru': ru,
                        'name_kk': kk,
                        'region_type': region_type,
                        'is_default': is_default,
                        'is_popular': is_popular,
                        'is_main': is_main,
                        'country': country_obj,
                        'parent': parent_obj,
                        'code': code,
                        'centroid': centroid,
                        'coordinates': coordinates
                        }
            utils_models.Region.objects.filter(code=code, parent=parent_obj).update_or_create(
                code=code,
                defaults=defaults
            )
            print(f"{ru} added/updated\n")
