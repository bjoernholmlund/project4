from django.shortcuts import render, redirect
from .models import Booking, Table
from .forms import BookingForm
from django.contrib import messages
from django.utils.timezone import now


# What does this view do?
# If a POST request is submitted, we create a booking.
# We check if the table is already booked at the selected time.
# If it is available, the booking is saved, otherwise the user receives an error message.

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
       form = bookingForm()

   return render(request, 'boookings/book_table.html', {'form': form})    



def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.delete()
    messages.success(request, " Your booking has been cancelled.")
    return redirect('book_table')