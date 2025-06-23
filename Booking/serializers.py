import binascii
from django.db import connection
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model
from .models import Property, Booking, Review

User = get_user_model()
user_table = User._meta.db_table
booking_table = Booking._meta.db_table
property_table = Property._meta.db_table

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField()

    def create(self, validated_data):
        hashed = make_password(validated_data['password'])
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {user_table} (email, first_name, last_name, phone, password, username)"
                " VALUES (%s, %s, %s, %s, %s, %s)",
                [
                    validated_data['email'],
                    validated_data['first_name'],
                    validated_data['last_name'],
                    validated_data['phone'],
                    hashed,
                    validated_data['email']  # username = email
                ]
            )
            cursor.execute("SELECT LAST_INSERT_ID()")
            user_id = cursor.fetchone()[0]
            cursor.execute(
                f"SELECT email, first_name, last_name, phone FROM {user_table} WHERE {User._meta.pk.column} = %s",
                [user_id]
            )
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return UserSerializer().create(validated_data)

class PropertySerializer(serializers.Serializer):
    house_id = serializers.IntegerField()
    owner_id = serializers.IntegerField(source='owner_id_id')
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_guests = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    country = serializers.CharField()
    region = serializers.CharField()
    street = serializers.CharField()
    city = serializers.CharField()
    house_number = serializers.CharField()
    apartment_number = serializers.CharField(allow_null=True, allow_blank=True)

class BookingSerializer(serializers.Serializer):
    booking_id     = serializers.IntegerField(read_only=True)
    house_id       = serializers.IntegerField()
    user_id        = serializers.IntegerField(read_only=True)
    check_in_date  = serializers.DateField()
    check_out_date = serializers.DateField()
    payment_id     = serializers.IntegerField(read_only=True)
    status         = serializers.CharField(read_only=True)
    created_at     = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT 1 FROM {booking_table}
                    WHERE house_id_id = %s
                      AND check_in_date < %s
                      AND check_out_date > %s""",
                [data['house_id'], data['check_out_date'], data['check_in_date']]
            )
            if cursor.fetchone():
                raise serializers.ValidationError("Obiekt w tym terminie jest już zarezerwowany!")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        status_val = 'confirmed'
        with connection.cursor() as cursor:

            cursor.execute(
                f"""INSERT INTO {booking_table}
                    (house_id_id, user_id_id, check_in_date, check_out_date, status, created_at)
                    VALUES (%s, %s, %s, %s, %s, NOW())""",
                [validated_data['house_id'], user.user_id,
                 validated_data['check_in_date'], validated_data['check_out_date'],
                 status_val]
            )
            cursor.execute("SELECT LAST_INSERT_ID()")
            booking_id = cursor.fetchone()[0]


            cursor.execute(
                f"""SELECT booking_id, house_id_id, user_id_id,
                           check_in_date, check_out_date,
                           payment_id_id, status, created_at
                    FROM {booking_table}
                    WHERE booking_id = %s""",
                [booking_id]
            )
            row = cursor.fetchone()
            cols = [col[0] for col in cursor.description]
        return dict(zip(cols, row))

class PaymentSerializer(serializers.Serializer):
    payment_id    = serializers.IntegerField(read_only=True)
    total_price   = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_status= serializers.ChoiceField(choices=[('pending','Pending'),('successful','Successful'),('cancelled','Cancelled')], default='pending')
    created_at    = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {Payment._meta.db_table}
                    (user_id_id, total_price, payment_status, created_at)
                    VALUES (%s, %s, %s, NOW())""",
                [user.id, validated_data['total_price'], validated_data['payment_status']]
            )
            cursor.execute("SELECT LAST_INSERT_ID()")
            payment_id = cursor.fetchone()[0]
            cursor.execute(
                f"SELECT payment_id, user_id_id, total_price, payment_status, created_at FROM {Payment._meta.db_table} WHERE payment_id = %s",
                [payment_id]
            )
            row = cursor.fetchone()
            cols = [c[0] for c in cursor.description]
        return dict(zip(cols, row))

class ReviewSerializer(serializers.Serializer):
    review_id   = serializers.IntegerField(read_only=True)
    user_id     = serializers.IntegerField(read_only=True)
    house_id    = serializers.IntegerField(write_only=True)
    rating      = serializers.IntegerField()
    description = serializers.CharField()
    created_at  = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        user    = self.context['request'].user
        house_id= validated_data['house_id']
        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {Review._meta.db_table}
                    (rating, description, created_at, house_id_id, user_id_id)
                   VALUES (%s, %s, NOW(), %s, %s)""",
                [
                    validated_data['rating'],
                    validated_data['description'],
                    house_id,
                    user.user_id
                ]
            )
            cursor.execute("SELECT LAST_INSERT_ID()")
            review_id = cursor.fetchone()[0]

            cursor.execute(
                f"""SELECT review_id,
                           rating,
                           description,
                           created_at,
                           house_id_id AS house_id,
                           user_id_id  AS user_id
                    FROM {Review._meta.db_table}
                    WHERE review_id = %s""",
                [review_id]
            )
            row = cursor.fetchone()
            cols = [col[0] for col in cursor.description]

        return dict(zip(cols, row))

class MessageSerializer(serializers.Serializer):
    message_id = serializers.IntegerField(read_only=True)
    receiver_id= serializers.IntegerField()
    content    = serializers.CharField()
    sent_at    = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        sender = self.context['request'].user
        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {Messages._meta.db_table}
                    (sender_id_id, receiver_id_id, content, sent_at)
                    VALUES (%s, %s, %s, NOW())""",
                [sender.id, validated_data['receiver_id'], validated_data['content']]
            )
            cursor.execute("SELECT LAST_INSERT_ID()")
            msg_id = cursor.fetchone()[0]
            cursor.execute(
                f"SELECT message_id, sender_id_id, receiver_id_id, content, sent_at FROM {Messages._meta.db_table} WHERE message_id = %s",
                [msg_id]
            )
            row = cursor.fetchone()
            cols = [c[0] for c in cursor.description]
        return dict(zip(cols, row))