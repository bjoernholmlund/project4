from django.contrib.auth.models import User # Import Django's User model
from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

def generate_unique_username():
    return f"some_unique_vale" #f"user_{uuid.uuid4().hex[:8]}"

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"


class Booking(models.Model):
    
    #Koppplar bokningen till en inloggad användare
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    # Om en användare inte är inloggad kan man fylla i dessa fält manuellt
    guest_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Name of the person booking (if not logged in)"
        )
    
    guest_email = models.EmailField(
        blank=True,
        help_text="Email of the person booking (if not logged in)"
        )
    
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date_time = models.DateTimeField(help_text="Format: YYYY-MM-DD HH:MM")
    number_of_guests = models.IntegerField(help_text="Number of guests")

    created_at = models.DateTimeField(default=timezone.now) 
    is_cancelled = models.BooleanField(default=False, help_text="Check if booking is cancelled")
 
    def __str__(self):
        if self.user:
            identifier = self.user.username
        else:
            identifier = self.guest_name or "Guest"    
            return f"Booking for {identifier} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"
     

class Menu(models.Model):
    name = models.CharField(max_length=215, help_text="Name of the dish")
    description = models.TextField(help_text="Description of the dish")
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Price of the dish")

    def __str__(self):
        return self.name

# KANSKE EN FORTSÄTTNING PÅ KODEN!

#class Order(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    #quantity = models.IntegerField()
    #created_at = models.DateTimeField(default=timezone.now)
    
    #def __str__(self):
    #    return f"{self.quantity} x {self.menu_item.name}"
    
    #def total_price(self):
    #    return self.quantity * self.menu_item.price    
    
