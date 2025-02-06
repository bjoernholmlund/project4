from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()


    def __str__(self):
        return f"table {self.table_number}"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    number_of_guests = models.IntegerField()

    def __str__(self):
        return f"Booking for {self.user} on {self.date_time}"
    
class Menu(models.Model):
    name = models.CharField(max_length=215)
    description = models.TextField()
    pårice = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name