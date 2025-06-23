# Booking/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    """
    Niestandardowy menedżer dla modelu User, który nie używa pola 'username'.
    """
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Usuwamy pole username
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=False, null=False)
    phone = models.CharField(max_length=9, blank=False, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = UserManager() # Używamy naszego menedżera

    def __str__(self):
        return self.email

# --- Pozostałe modele bez zmian ---

class Property(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_properties")
    house_id = models.AutoField(primary_key=True)
    # ... reszta pól bez zmian
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    max_guests = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=255, blank=False, null=False)
    region = models.CharField(max_length=255, blank=False, null=False)
    street = models.CharField(max_length=255, blank=False, null=False)
    city = models.CharField(max_length=255, blank=False, null=False)
    house_number = models.CharField(max_length=255, blank=False, null=False)
    apartment_number = models.CharField(max_length=255, blank=True, null=True)

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    # ... reszta pól bez zmian
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('successful', 'Successful'), ('cancelled', 'Cancelled')])
    created_at = models.DateTimeField(auto_now_add=True)

class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    # ... reszta pól bez zmian
    content = models.TextField(blank=False, null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    house_id = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    # ... reszta pól bez zmian
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    payment_id = models.ForeignKey(Payment, null=True, on_delete=models.CASCADE, related_name='booking')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    house_id = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    # ... reszta pól bez zmian
    rating = models.IntegerField()
    description = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    house_id = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')

class Amenities(models.Model):
    house_id = models.OneToOneField(Property, on_delete=models.CASCADE, primary_key=True, related_name='amenities')
    # ... reszta pól bez zmian
    parking_lot = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    sauna = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    house_id = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    # ... reszta pól bez zmian
    image_url = models.CharField(max_length=255, null=False, blank=False)
    is_main = models.BooleanField(default=False)