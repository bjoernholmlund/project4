from django.urls import path
from . import views
from .views import book_table, cancel_booking



urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('book/', book_table, name='book_table'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
]

