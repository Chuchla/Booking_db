# Booking/routers.py
import random

class ReadReplicaRouter:
    """
    Router, który kieruje odczyty do losowej repliki (lub mastera),
    a wszystkie zapisy do bazy 'default' (master).
    """
    def db_for_read(self, model, **hints):
        # Rozkłada zapytania odczytu 50/50 między mastera a replikę
        return random.choice(['default', 'replica'])

    def db_for_write(self, model, **hints):
        # Wszystkie zapisy idą do mastera
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Pozwala na relacje między obiektami w tej samej bazie
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Migracje wykonujemy tylko na masterze
        return db == 'default'