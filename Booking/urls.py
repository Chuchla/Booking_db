from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('property/create/', PropertyCreateView.as_view(), name='property_create'),
    path('property/search/', PropertySearchView.as_view(), name='property_search'),
    path('property/<int:house_id>/', PropertyGetView.as_view(), name='property_get'),
    path('booking/create/', BookingCreateView.as_view(), name='booking_create'),
    path('booking/<int:house_id>/', PropertyGetBookingsView.as_view(), name='booking_get'),

path('payment/create/',       PaymentCreateView .as_view(), name='payment_create'),
path('message/send/',         MessageCreateView .as_view(), name='message_send'),
path('review/create/',        ReviewCreateView  .as_view(), name='review_create')

]
