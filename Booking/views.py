import os
import binascii
import logging
from datetime import datetime
from django.db import connection
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Property, Booking, User
from .serializers import PropertySerializer, BookingSerializer, PaymentSerializer, MessageSerializer, ReviewSerializer

logger = logging.getLogger(__name__)

table_user = User._meta.db_table
user_pk_col = User._meta.pk.column
booking_table = Booking._meta.db_table
property_table = Property._meta.db_table

def get_token_table():
    return 'authtoken_token'

class PropertySearchView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        region      = request.query_params.get('region')
        city        = request.query_params.get('city')
        min_price   = request.query_params.get('minP')
        max_price   = request.query_params.get('maxP')
        min_guests  = request.query_params.get('minG')
        max_guests  = request.query_params.get('maxG')
        country     = request.query_params.get('country')
        description = request.query_params.get('description')
        check_in    = request.query_params.get('checkIn')
        check_out   = request.query_params.get('checkOut')


        prop_table = Property._meta.db_table
        book_table = Booking._meta.db_table
        fk_col     = Booking._meta.get_field('house_id').column
        pk_col     = Property._meta.get_field('house_id').column


        sql_parts = [f"SELECT p.* FROM {prop_table} p"]
        params = []
        if check_in and check_out:
            sql_parts.append(f"""
                LEFT JOIN {book_table} b
                  ON b.{fk_col}      = p.{pk_col}
                 AND b.status        = 'confirmed'
                 AND b.check_in_date < %s
                 AND b.check_out_date> %s
            """)
            params += [check_out, check_in]

        sql_parts.append("WHERE 1=1")
        if region:
            sql_parts.append("AND p.region = %s")
            params.append(region)
        if city:
            sql_parts.append("AND p.city = %s")
            params.append(city)
        if min_price:
            sql_parts.append("AND p.price >= %s")
            params.append(min_price)
        if max_price:
            sql_parts.append("AND p.price <= %s")
            params.append(max_price)
        if min_guests:
            sql_parts.append("AND p.max_guests >= %s")
            params.append(min_guests)
        if max_guests:
            sql_parts.append("AND p.max_guests <= %s")
            params.append(max_guests)
        if country:
            sql_parts.append("AND p.country = %s")
            params.append(country)
        if description:
            sql_parts.append("AND p.description LIKE %s")
            params.append(f"%{description}%")


        if check_in and check_out:
            sql_parts.append("AND b.booking_id IS NULL")


        final_sql = "\n".join(sql_parts)
        final_sql += " LIMIT 50"
        logger.debug("RAW SQL:\n%s", final_sql)
        logger.debug("PARAMS: %r", params)


        queryset = Property.objects.raw(final_sql, params)
        return Response(PropertySerializer(queryset, many=True).data)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email i hasło są wymagane.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT {user_pk_col}, password FROM {table_user} WHERE email = %s",
                    [email]
                )
                row = cursor.fetchone()

            if not row or not check_password(password, row[1]):
                return Response({'error': 'Nieprawidłowe dane logowania.'}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = row[0]
            token_table = get_token_table()

            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT `key` FROM {token_table} WHERE user_id = %s",
                    [user_id]
                )
                token_row = cursor.fetchone()

                if token_row:
                    token = token_row[0]
                else:

                    token = binascii.hexlify(os.urandom(20)).decode()


                    cursor.execute(
                        f"INSERT INTO {token_table} (`key`, user_id, created) VALUES (%s, %s, NOW())",
                        [token, user_id]
                    )

            return Response({'token': token})

        except Exception as e:
            logger.error(f"Błąd podczas logowania: {e}")
            return Response({'error': 'Wystąpił nieoczekiwany błąd serwera.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone = request.data.get('phone')
        password = request.data.get('password')

        if not all([email, first_name, last_name, phone, password]):
            return Response({'error': 'Wszystkie pola są wymagane.'}, status=status.HTTP_400_BAD_REQUEST)

        username = email
        hashed_password = make_password(password)


        is_active = True
        is_staff = False
        is_superuser = False

        try:
            with connection.cursor() as cursor:

                sql = (
                    f"INSERT INTO {table_user} "
                    "(username, first_name, last_name, email, password, phone, "
                    "is_active, is_staff, is_superuser, date_joined) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"
                )
                cursor.execute(sql, [
                    username, first_name, last_name, email, hashed_password, phone,
                    is_active, is_staff, is_superuser
                ])

            return Response({'message': 'Rejestracja zakończona sukcesem.'}, status=status.HTTP_201_CREATED)

        except Exception as e:

            if 'Duplicate entry' in str(e) and 'for key' in str(e):
                return Response({'error': 'Użytkownik z tym adresem e-mail już istnieje.'},
                                status=status.HTTP_400_BAD_REQUEST)


            logger.error(f"Błąd podczas rejestracji: {e}")
            return Response({'error': 'Wystąpił nieoczekiwany błąd podczas rejestracji.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PropertyCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        data = request.data

        fields = [
            'name', 'description', 'price', 'max_guests',
            'country', 'region', 'street', 'city',
            'house_number', 'apartment_number'
        ]
        values = [data.get(f) for f in fields]

        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {property_table} (owner_id_id, {', '.join(fields)}, created_at)"
                f" VALUES (%s, {', '.join(['%s']*len(fields))}, NOW())",
                [user.user_id] + values
            )
            cursor.execute("SELECT LAST_INSERT_ID()")
            house_id = cursor.fetchone()[0]

            from django.db import connections
            with connections['default'].cursor() as master_cursor:
                master_cursor.execute(
                    f"SELECT * FROM {property_table} WHERE house_id = %s",
                    [house_id]
                )
                row = master_cursor.fetchone()
                columns = [col[0] for col in master_cursor.description]
        result = dict(zip(columns, row))
        return Response(result, status=status.HTTP_201_CREATED)


class PaymentCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        return Response(payment, status=status.HTTP_201_CREATED)


class PropertyGetView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, house_id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {property_table} WHERE house_id = %s",
                [house_id]
            )
            row = cursor.fetchone()
            if not row:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            columns = [col[0] for col in cursor.description]
        return Response(dict(zip(columns, row)))

class BookingCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response(booking, status=status.HTTP_201_CREATED)

class PropertyGetBookingsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, house_id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {booking_table} WHERE house_id_id = %s",
                [house_id]
            )
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, r)) for r in rows]
        return Response(result)

class MessageCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        msg = serializer.save()
        return Response(msg, status=status.HTTP_201_CREATED)

class ReviewCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=400)
        try:
            review = serializer.save()
            return Response(review, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Exception during save:", str(e))
            return Response({"detail": str(e)}, status=500)
