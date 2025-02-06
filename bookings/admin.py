from django.contrib import admin
from .models import User, Table, Booking, Menu

# Register your models here

admin.site.register(User)
admin.site.register(Table)
admin.site.register(Booking)
admin.site.register(Menu)