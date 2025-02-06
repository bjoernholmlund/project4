from django.urls import path
from .views import book_table
from .views import cancel_booking

urlpatterns = [
    path('book/', book_table, name='book_table'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
]

