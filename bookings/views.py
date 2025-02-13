from django.shortcuts import render, redirect
from .models import Booking
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

def UserCreationForm(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Logga in användaren direkt efter registrering
            return redirect('home')  # Eller någon annan sida du vill skicka användaren till
    else:
        form = UserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})

def book_table(request):
   if request.method == 'Post':
      form = BookingForm(request.Post)
      if form.is_valid():
            booking_date = form.cleaned_data['data_time']
            table = form.cleaned_data['table']


            # Check if the table is available on that date
      existing_booking = Booking.objects.filter(table=table, date_time=booking_date).exists()

      if existing_booking:
           messages.error(request, "The table is already booked at this time. Choose another time or another table.")        
        
      else:
         form.save()
         messages.success(request, "Your booking is confirmed!")
         return redirect('book_table') # Send back to the booking page or a confirmation page
        
   else:
       form = BookingForm()

   return render(request, 'boookings/book_table.html', {'form': form})    



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
