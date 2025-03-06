import datetime
from django.shortcuts import render, redirect
from .models import Booking, Table
from .forms import BookingForm, RegisterForm, AuthenticateForm, UserCreationForm
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# What does this view do?
# If a POST request is submitted, we create a booking.
# We check if the table is already booked at the selected time.
# If it is available, the booking is saved, otherwise the user receives an error message.

@login_required
def profile(request):
    return render(request, 'bookings/profile.html')
def index(request):
    return render(request, 'bookings/index.html')
def base_view(request):
    return render(request, 'bookings/base.html')
def UserCreationForm(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registration.
            return redirect('home')  # Or any other page you want to send the user to.
    else:
        form = UserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})

def book_table(request):
    if request.method == 'POST':  
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_date = form.cleaned_data['date_time']
            table = form.cleaned_data['table']
            guest_name = form.cleaned_data['guest_name']
            guest_email = form.cleaned_data['guest_email']
            
            # Rundar bokningstid till närmaste minut
            rounded_booking_date = booking_date.replace(second=0, microsecond=0)

            # Kontrollera om bordet redan är bokat vid exakt denna tid
        existing_booking = Booking.objects.filter(
            table=table,
            date_time__lt=rounded_booking_date + datetime.timedelta(hours=3),
            date_time__gt=rounded_booking_date
            ).exists()

        if existing_booking:
                messages.error(request, "The table is already booked at this time. Choose another time or another table.")
                return render(request, 'bookings/book_table.html', {'form': form})  # Viktigt att returnera här!

            # Om användaren inte är inloggad, se till att namn och e-post är ifyllda
        if not request.user.is_authenticated:
                if not guest_name or not guest_email:
                    messages.error(request, "Please provide both your name and email address if you're not logged in.")
                    return render(request, 'bookings/book_table.html', {'form': form})

        form.save()
        messages.success(request, "Your booking is confirmed!")
        return redirect('book_table') 

    else:
        form = BookingForm()

    return render(request, 'bookings/book_table.html', {'form': form})
     


def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    
    if request.user == booking.user: # Ensure the correct user cancels
       booking.delete()
       messages.success(request, " Your booking has been cancelled.")
    else:
        messages.error(request, "You are not authorized to cancel this booking.")

    return redirect('book_table')

def register(request):
   if request.method == 'POST':
      form = RegisterForm(request.POST)
      if form.is_valid():
         user = form.save()
         login(request, user) # Log in immediately after registration
         messages.success(request, "Registration successful! You are now logged in.")
         return redirect('book_table')

   else:
      form = RegisterForm()
   return render(request, 'bookings/register.html', {'form': form})

def login_view(request):
   if request.method == 'POST':
      form = AuthenticateForm(data=request.POST)
      if form.is_valid():
         user = form.get_user()
         login(request, user)
         messages.success(request, "You are now logged in!")
         return redirect('book_table')
         
   else:
      form = AuthenticateForm()
   return render(request, 'bookings/login.html', {'form': form})   

def logout_view(request):
    logout(request)
    messages.success(request, "You are now logged out!")
    return redirect('login')


def create_booking(request):
    tables = Table.objects.all() # Getting all the tables
    if request.method == "POST":
       form = BookingForm(request.POST)
       if form.is_valid():
            form.save()
            return redirect('bookings:book_table')
       else:
           form = BookingForm()    
       return render/request, 'bookings/create_booking.html', {'form': form, 'tables': tables}    