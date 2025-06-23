import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import connection, transaction, IntegrityError
from faker import Faker # Faker jest przydatny, zostawmy go na przyszłość

class Command(BaseCommand):
    help = 'Populates the database with a specified number of property objects.'

    def add_arguments(self, parser):
        # Dodajemy opcjonalny argument, aby móc określić liczbę obiektów z linii komend
        parser.add_argument(
            '--number',
            type=int,
            help='Specifies the number of properties to create',
            default=50000  # Domyślna wartość, jeśli nie podamy
        )

    def handle(self, *args, **options):
        NUMBER_OF_PROPERTIES = options['number']
        OWNER_ID = 1  # Zakładamy, że użytkownik o ID=1 istnieje i będzie właścicielem

        # Przykładowe dane do losowania (z Twojego skryptu)
        cities = ['Warszawa', 'Kraków', 'Gdańsk', 'Wrocław', 'Poznań', 'Mielno']
        countries = ['Polska']
        regions = ['Mazowieckie', 'Małopolskie', 'Pomorskie', 'Dolnośląskie', 'Wielkopolskie']
        sample_descriptions = ['Przytulny apartament w centrum.', 'Nowoczesne studio z widokiem na park.', 'Willa z ogrodem i basenem.', 'Loft w stylu industrialnym.', 'Zawiera ślady azbestu.']

        self.stdout.write(f"Rozpoczynam wstawianie {NUMBER_OF_PROPERTIES} obiektów...")

        try:
            # Używamy `transaction.atomic`, aby wszystkie operacje INSERT
            # zostały wykonane w jednej, dużej transakcji. To jest ZNACZNIE szybsze.
            with transaction.atomic():
                # Używamy `connection.cursor()`, aby dostać się do "surowego" kursora
                with connection.cursor() as cursor:
                    for i in range(NUMBER_OF_PROPERTIES):
                        property_data = {
                            'owner_id': OWNER_ID,
                            'name': f'Obiekt Testowy numer {i}',
                            'description': random.choice(sample_descriptions),
                            'price': Decimal(random.randrange(150, 1000)),
                            'max_guests': random.randint(1, 10),
                            'country': random.choice(countries),
                            'region': random.choice(regions),
                            'city': random.choice(cities),
                            'street': f'Ulica Testowa {i}',
                            'house_number': str(random.randint(1, 200))
                        }

                        # Twoje zapytanie SQL jest idealne, zostaje bez zmian
                        add_property = ("INSERT INTO Booking_property "
                                        "(owner_id, name, description, price, max_guests, country, region, city, street, house_number, created_at) "
                                        "VALUES (%(owner_id)s, %(name)s, %(description)s, %(price)s, %(max_guests)s, %(country)s, %(region)s, %(city)s, %(street)s, %(house_number)s, NOW())")

                        # W Django, dla surowych zapytań, owner_id to po prostu owner_id, nie owner_id_id
                        # Poprawmy to dla spójności
                        add_property_django = ("INSERT INTO Booking_property "
                                               "(owner_id_id, name, description, price, max_guests, country, region, city, street, house_number, created_at) "
                                               "VALUES (%(owner_id)s, %(name)s, %(description)s, %(price)s, %(max_guests)s, %(country)s, %(region)s, %(city)s, %(street)s, %(house_number)s, NOW())")


                        cursor.execute(add_property_django, property_data)

                        if (i + 1) % 1000 == 0:
                            self.stdout.write(f"Wstawiono {i + 1}/{NUMBER_OF_PROPERTIES} obiektów...")

            self.stdout.write(self.style.SUCCESS(f"Sukces! Dodano {NUMBER_OF_PROPERTIES} obiektów do bazy."))

        except IntegrityError as e:
            # Ten błąd może się pojawić, jeśli np. próbujemy dodać obiekt dla owner_id, który nie istnieje
            self.stderr.write(self.style.ERROR(f'Błąd integralności danych: {e}. Upewnij się, że użytkownik o ID={OWNER_ID} istnieje.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Wystąpił nieoczekiwany błąd: {e}"))