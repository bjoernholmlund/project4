from django.urls import path
from .views import book_table

urlpatterns = [
    path('book/', book_table, name='book_table'),
]

