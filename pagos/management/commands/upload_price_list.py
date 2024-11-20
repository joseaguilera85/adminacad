from django.core.management.base import BaseCommand
from apartments.models import Project, Apartment
from pagos.models import PriceList

class Command(BaseCommand):
    help = 'Uploads the price list for apartments'

    def handle(self, *args, **kwargs):
        price_list_data = [
    {"project_name": "Proyecto A", "apartment_number": "103", "prices": [100000, 105000, 110000, 115000, 120000, 125000], "current_price_index": 0},
    {"project_name": "Proyecto A", "apartment_number": "104", "prices": [100000, 105000, 110000, 115000, 120000, 125000], "current_price_index": 0},
    
    # Proyecto B
    {"project_name": "Proyecto B", "apartment_number": "202", "prices": [200000, 210000, 220000, 230000, 240000, 250000], "current_price_index": 0},
    {"project_name": "Proyecto B", "apartment_number": "203", "prices": [200000, 210000, 220000, 230000, 240000, 250000], "current_price_index": 0},
    {"project_name": "Proyecto B", "apartment_number": "204", "prices": [200000, 210000, 220000, 230000, 240000, 250000], "current_price_index": 0},
    
    # Proyecto C
    {"project_name": "Proyecto C", "apartment_number": "301", "prices": [300000, 315000, 330000, 345000, 360000, 375000], "current_price_index": 0},
    {"project_name": "Proyecto C", "apartment_number": "302", "prices": [300000, 315000, 330000, 345000, 360000, 375000], "current_price_index": 0},
    {"project_name": "Proyecto C", "apartment_number": "303", "prices": [300000, 315000, 330000, 345000, 360000, 375000], "current_price_index": 0},
    {"project_name": "Proyecto C", "apartment_number": "304", "prices": [300000, 315000, 330000, 345000, 360000, 375000], "current_price_index": 0},
    
    # Proyecto D
    {"project_name": "Proyecto D", "apartment_number": "401", "prices": [400000, 420000, 440000, 460000, 480000, 500000], "current_price_index": 0},
    {"project_name": "Proyecto D", "apartment_number": "402", "prices": [400000, 420000, 440000, 460000, 480000, 500000], "current_price_index": 0},
    {"project_name": "Proyecto D", "apartment_number": "403", "prices": [400000, 420000, 440000, 460000, 480000, 500000], "current_price_index": 0},
    {"project_name": "Proyecto D", "apartment_number": "404", "prices": [400000, 420000, 440000, 460000, 480000, 500000], "current_price_index": 0},
            # Add other data entries here
        ]

        for data in price_list_data:
            project, _ = Project.objects.get_or_create(name=data["project_name"])
            apartment, _ = Apartment.objects.get_or_create(number=data["apartment_number"], project=project)
            
            price_list = PriceList.objects.create(
                project=project,
                apartment=apartment,
                list_number_0=data["prices"][0],
                list_number_1=data["prices"][1],
                list_number_2=data["prices"][2],
                list_number_3=data["prices"][3],
                list_number_4=data["prices"][4],
                list_number_5=data["prices"][5],
                current_list_price_index=data["current_price_index"],
            )

            self.stdout.write(self.style.SUCCESS(f'Created PriceList for Apartment {apartment.number} in Project {project.name}'))
