import datetime
from django.contrib.auth.models import User # Import Django's User model
from django.db import models
from django.forms import ValidationError
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

from restaurant_booking import settings

# Create your models here.

def generate_unique_username():
    return f"some_unique_vale" #f"user_{uuid.uuid4().hex[:8]}"

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"


class Booking(models.Model):
    TABLE_DURATION = datetime.timedelta(hours=2, minutes=59)  # ⏳ Bokningstid 3h

    table = models.ForeignKey("bookings.Table", on_delete=models.CASCADE, null=False, blank=False)
    date_time = models.DateTimeField(help_text="Format: YYYY-MM-DD HH:MM")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    guest_name = models.CharField(max_length=100, blank=True, help_text="Name of the person booking (if not logged in)")
    guest_email = models.EmailField(blank=True, help_text="Email of the person booking (if not logged in)")
    number_of_guests = models.IntegerField(help_text="Number of guests")

    created_at = models.DateTimeField(default=timezone.now)
    is_cancelled = models.BooleanField(default=False, help_text="Check if booking is cancelled")

    class Meta:
        unique_together = ("table", "date_time")

    @property
    def end_time(self):
        return self.date_time + self.TABLE_DURATION

    def clean(self):
        if not self.table:
            raise ValidationError("Please select a table.")
        
        # Kolla öppettider
        weekday = self.date_time.strftime("%A").lower()
        opening_time, closing_time = settings.OPENING_HOURS.get(weekday, ("00:00", "00:00"))

        opening_dt = datetime.datetime.strptime(opening_time, "%H:%M").time()
        closing_dt = datetime.datetime.strptime(closing_time, "%H:%M").time()

        if not (opening_dt <= self.date_time.time() <= closing_dt):
            raise ValidationError(f"Bookings are only allowed between {opening_time} and {closing_time} on {weekday.capitalize()}.")

        # Kolla om bokningen krockar med en annan
        overlapping_bookings = Booking.objects.filter(
            table=self.table,
            date_time__lt=self.end_time,  # Ny bokning startar innan den gamla slutar
            date_time__gte=self.date_time - self.TABLE_DURATION  # Ny bokning slutar efter den gamla startar
        ).exclude(id=self.id)

        if overlapping_bookings.exists():
            raise ValidationError(f"The table {self.table} is already booked at this time. Choose another time or another table.")

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
    category = models.CharField(max_length=50, blank=True, null=True, help_text="Category of the dish") # Ex: "Appetizer", "Main course"
    # Probably not using this field
    #image = models.ImageField(upload_to="menu_images", blank=True, null=True, help_text="Image of the dish")

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
    
