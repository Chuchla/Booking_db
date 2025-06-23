# Booking/routers.py

import random

class DatabaseRouter:
    """
    Router bazy danych, który:
    1. Kieruje operacje zapisu do bazy 'default' (master).
    2. Równoważy (rozdziela) operacje odczytu pomiędzy bazę 'default' (master)
       i bazę 'slave'.
    """

    def db_for_read(self, model, **hints):
        """
        Losowo wybiera bazę danych ('default' lub 'slave') dla operacji odczytu.
        """
        return random.choice(['default', 'slave'])

    def db_for_write(self, model, **hints):
        """
        Zawsze kieruje operacje zapisu do bazy 'default' (master).
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Zezwala na relacje między obiektami.
        """
        # Zezwalaj na relacje, jeśli obie bazy są w naszej puli
        db_list = ('default', 'slave')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Upewnia się, że migracje są uruchamiane tylko na bazie master ('default').
        """
        return db == 'default'