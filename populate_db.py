import mysql.connector
import random
from decimal import Decimal

# Ustaw dane do połączenia z bazą (takie jak w settings.py)
config = {
    'user': 'booking_user',
    'password': 'password123', # Twoje hasło
    'host': '127.0.0.1',
    'database': 'db_booking',
    'raise_on_warnings': True
}

# Przykładowe dane do losowania
cities = ['Warszawa', 'Kraków', 'Gdańsk', 'Wrocław', 'Poznań', 'Mielno']
countries = ['Polska']
regions = ['Mazowieckie', 'Małopolskie', 'Pomorskie', 'Dolnośląskie', 'Wielkopolskie']
sample_descriptions = ['Przytulny apartament w centrum.', 'Nowoczesne studio z widokiem na park.', 'Willa z ogrodem i basenem.', 'Loft w stylu industrialnym.', 'Zawiera ślady azbestu.']

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Ustaw, ile obiektów chcesz dodać
    NUMBER_OF_PROPERTIES = 50000
    # Załóżmy, że użytkownik o ID=1 istnieje i będzie właścicielem
    OWNER_ID = 1

    print(f"Rozpoczynam wstawianie {NUMBER_OF_PROPERTIES} obiektów...")

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

        add_property = ("INSERT INTO Booking_property "
                        "(owner_id_id, name, description, price, max_guests, country, region, city, street, house_number, created_at) "
                        "VALUES (%(owner_id)s, %(name)s, %(description)s, %(price)s, %(max_guests)s, %(country)s, %(region)s, %(city)s, %(street)s, %(house_number)s, NOW())")

        cursor.execute(add_property, property_data)

        if (i + 1) % 1000 == 0:
            print(f"Wstawiono {i + 1}/{NUMBER_OF_PROPERTIES} obiektów...")

    # Zatwierdź transakcję
    cnx.commit()

except mysql.connector.Error as err:
    print(f"Błąd bazy danych: {err}")
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'cnx' in locals() and cnx.is_connected():
        cnx.close()
    print("Zakończono. Połączenie z bazą zamknięte.")