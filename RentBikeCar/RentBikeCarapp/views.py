from django.shortcuts import render, redirect, HttpResponse
from .models import BikeType, Bike, Rental, Payment, Gallery, Document, Booking, Review
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail, get_connection, EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
import pytz
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat
from django.utils.timezone import make_aware, localtime
from django.contrib.auth import update_session_auth_hash


@login_required(login_url="/login")  
def index(request):
    bikes = Bike.objects.all()
    us = request.user
    #now = make_aware(datetime.now())
    
    bike_statuses = {}
        
    now = datetime.utcnow().replace(tzinfo=pytz.utc)

    for bike in bikes:
        
        books = Booking.objects.filter(user=request.user, bike_id=bike.bike_id)
        
       
        is_available = True 
        for book in books:
            ist = pytz.timezone('Asia/Kolkata')
            end_datetime_ist = book.end_time.astimezone(ist)
            end_time_ist = localtime(end_datetime_ist, ist)
            print(end_time_ist)
            if end_time_ist < now:
                # If booking has ended, bike should be available
                is_available = True
            else:
                # If there's an active booking, bike should not be available
                is_available = False
                break 
        
        bike.is_available = is_available
        bike.save()
        
        bike_statuses[bike.bike_id] = bike.is_available
            
        
        reviews = Review.objects.filter(bike=bike)
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / reviews.count()
        else:
            average_rating = 0
        
        bike.average_rating = average_rating

    context = {
        'user': us,
        'bikes': bikes,
        'bike_statuses': bike_statuses
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            messages.error(request, 'Please fill in all fields.')
        else:
            email_subject = f"New Contact Us Message from {name}"
            email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            # Send the email
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Replace with your contact email
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully.')

    return render(request, 'index.html', context)






def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return render(request, 'register.html')

        # Create user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect('/login')

    return render(request, 'register.html')
    
    

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')
    
@login_required(login_url="/login")    
def user_logout(request):
  
  logout(request)
  
  
  return redirect('/')   
        
         
     
def gallery(request):
    
    if request.method == "GET":
        
        return render(request, 'gallery.html')
    
    else:
        
        image = request.FILES['image']
        
        gallery = Gallery.objects.create(image = image)
        
        gallery.save()
        
        return HttpResponse("Done")
    

def forgot_passward(request):
  
  if request.method == "GET":
    
    return render(request, 'forgotpass.html')
  
  else:
    
    email = request.POST['email']
    
    request.session['email'] = email
    
    user = User.objects.filter(email = email).exists()
    
    if user:
      
    
      otp = random.randint(1000, 9999)
      
      request.session['otp'] = otp
      
      with get_connection(
        
        host = settings.EMAIL_HOST, 
        port= settings.EMAIL_PORT ,
        use_tls= settings.EMAIL_USE_TLS,
        username= settings.EMAIL_HOST_USER, 
        passward = settings.EMAIL_HOST_PASSWORD 
      ) as connection :
        
        subject = "Email from django"
        message = f"OTP is {otp} and send pyment on https://razorpay.me/@darshansureshdevmore"  
        email_from = settings.EMAIL_HOST_USER
        reciption_list = [ email ]
        
        EmailMessage(subject, message, email_from, reciption_list, connection= connection).send()
      
        return redirect("/otp_verification")
      
    else:
      
      context = {}
      
      context['error'] = "Email Doest Not Exists" 
      
      return render(request, "forgotpass.html", context)
    

def otp_verification(request):
  
  if request.method == "GET":
    
    return render(request, 'otp.html')
  
  else:
    
    otp = int(request.POST['otp'])
    
    otp_email = int(request.session['otp'])
    
    if otp == otp_email:
      
      return redirect('/newpassword')
      
    else:
      
      return HttpResponse("Not ok")
    
def newpassword(request):
  
  if request.method == 'GET':
    
    return render(request, 'newpassword.html')
  
  else:
    
    email = request.session['email']
    
    password = request.POST['password']
    confirm_pass = request.POST['confirm_pass']
    
    user = User.objects.get(email = email)
    
    if password == confirm_pass:
      
      user.set_password(password)
      
      user.save()
      
      return redirect('/login')
    
    else:
      
      context = {}
      
      context['error'] = "Password and Confirm Password Does Not Match"
      
      return render(request, 'newpassword.html', context)     
    
         

# BikeType Views
@login_required(login_url="/login")
def bike_type_list(request):
    bike_types = BikeType.objects.all()
    context = {'data': bike_types}
    return render(request, 'bike_type_list.html', context)

@login_required(login_url="/login")
def bike_type_detail(request, rid):
    bike_type = BikeType.objects.get(id=rid)
    context = {'data': bike_type}
    return render(request, 'bike_type_detail.html', context)

@login_required(login_url="/login")
def bike_type_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        BikeType.objects.create(name=name, description=description)
        return redirect('bike_type_list')
    return render(request, 'bike_type_form.html')

@login_required(login_url="/login")
def bike_type_update(request, rid):
    bike_type = BikeType.objects.get(id=rid)
    if request.method == 'POST':
        bike_type.name = request.POST.get('name')
        bike_type.description = request.POST.get('description')
        bike_type.save()
        return redirect('bike_type_detail', rid=rid)
    context = {'bike_type': bike_type}
    return render(request, 'bike_type_form.html', context)

@login_required(login_url="/login")
def bike_type_delete(request, rid):
    bike_type = BikeType.objects.get(id=rid)
    if request.method == 'POST':
        bike_type.delete()
        return redirect('bike_type_list')
    context = {'bike_type': bike_type}
    return render(request, 'bike_type_confirm_delete.html', context)

# Bike Views
@login_required(login_url="/login")
def bike_list(request):
    bikes = Bike.objects.all()
    for bike in bikes:
        print(f'Bike ID: {bike.bike_id}, Bike Name: {bike.name}')
    context = {'bikes': bikes}
    return render(request, 'bike_list.html', context)

@login_required(login_url="/login")
def bike_detail(request, rid):
    bike = Bike.objects.get(bike_id=rid)
    context = {'bike': bike}
    return render(request, 'bike_detail.html', context)

@login_required(login_url="/login")
def bike_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        bike_type_id = request.POST.get('bike_type')  # Get bike_type id from form
        bike_type = BikeType.objects.get(id=bike_type_id)  # Retrieve BikeType object
        category = request.POST.get('category')
        is_available = request.POST.get('is_available') == 'on'
        hourly_rate = request.POST.get('hourly_rate')
        image = request.FILES.get('image')
        year = request.POST.get('year')
        location_details = request.POST.get('location_details')
        location = request.POST.get('location')
        deposit = request.POST.get('deposit')
        original_rate = request.POST.get('original_rate')
        
        # Create Bike object with retrieved data
        Bike.objects.create(name=name, bike_type=bike_type, is_available=is_available, hourly_rate=hourly_rate, image=image, 
                            original_rate = original_rate, year =year, location_details= location_details, location= location, deposit = deposit, category =category  )
        
        return redirect('bike_list')  # Redirect to bike list view after creation
    bike_types = BikeType.objects.all()
    
    context ={}
    
    context['bike_types'] = bike_types
    
    return render(request, 'bike_create.html', context)

@login_required(login_url="/login")
def bike_update(request, rid):
    bike = Bike.objects.get(bike_id=rid)
    bike_types = BikeType.objects.all()
    
    if request.method == 'POST':
        bike.name = request.POST.get('name')
        bike.bike_type = BikeType.objects.get(id=request.POST.get('bike_type'))
        bike.is_available = request.POST.get('is_available') == 'on'
        bike.hourly_rate = request.POST.get('hourly_rate')
        
        if request.FILES.get('image'):  
            bike.image = request.FILES.get('image')
        
        bike.save()
        return redirect('bike_detail', rid=rid)  
    
    context = {'bike': bike, 'bike_types': bike_types}
    return render(request, 'bike_form.html', context)

@login_required(login_url="/login")
def bike_delete(request, rid):
    bike = Bike.objects.get(bike_id=rid)
    if request.method == 'POST':
        bike.delete()
        return redirect('bike_list')
    context = {'bike': bike}
    return render(request, 'bike_confirm_delete.html', context)

# Rental Views
@login_required(login_url="/login")
def rental_list(request):
    rentals = Rental.objects.all()
    context = {'rentals': rentals}
    return render(request, 'rental_list.html', context)

@login_required(login_url="/login")
def rental_detail(request, rid):
    rental = Rental.objects.get(id=rid)
    context = {'rental': rental}
    return render(request, 'rental_detail.html', context)

# Payment Views
@login_required(login_url="/login")
def payment_list(request):
    payments = Payment.objects.all()
    context = {'payments': payments}
    return render(request, 'payment_list.html', context)

@login_required(login_url="/login")
def payment_detail(request, rid):
    payment = Payment.objects.get(id=rid)
    context = {'payment': payment}
    return render(request, 'payment_detail.html', context)



@login_required(login_url = "/login")
def more(request):
    
    return render(request, 'more.html')


def rentbycategory(request, category):
    bikes = Bike.objects.filter(category=category)
    categories = BikeType.objects.all()  # This assumes you have a list of bike types

    context = {
        'bikes': bikes,
        'categories': categories,
        'selected_category': category
    }
    return render(request, 'rentbycategory.html', context)


@login_required(login_url="/login")
def contact(request):
    success = False
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        
        # Construct the email message
        email_subject = f"New Contact Us Message from {name}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        # Send the email
        send_mail(
            email_subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],  # Replace with your contact email
            fail_silently=False,
        )
        
        success = True

    return render(request, 'contact.html', {'success': success})

@login_required(login_url="/login")
def upload_documents(request, bike_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        adhar = request.FILES.get('adhar')
        driving_licence = request.FILES.get('driving_licence')

        if name and adhar and driving_licence:
            bike = Bike.objects.filter(bike_id=bike_id).first()
            if bike:
                Document.objects.create(
                    name=name,
                    adhar=adhar,
                    driving_licence=driving_licence,
                    bike=bike,
                    user=request.user
                )
                return redirect('vehicledetails', rid=bike_id)
            else:
                return HttpResponse("Bike not found.")
        else:
            return HttpResponse("All fields are required.")
    return HttpResponse("Invalid request method.")


from django.utils import timezone


@login_required(login_url="/login")
def submit_pickup_time(request, bike_id):
    if request.method == 'POST':
        bike = Bike.objects.filter(bike_id=bike_id).first()
        if not bike:
            return HttpResponse("Bike not found.")
        
        pickup_time = request.POST.get('pickup_time')
        hours = int(request.POST.get('hours', 1))
        
        if pickup_time:
            try:
                # Parse the pickup time from user input (assumed to be in IST)
                pickup_datetime = datetime.strptime(pickup_time, '%Y-%m-%dT%H:%M')
                ist = pytz.timezone('Asia/Kolkata')
                pickup_datetime = ist.localize(pickup_datetime)
                
                # Convert pickup_datetime to UTC for database consistency
                pickup_datetime_ist = pickup_datetime.astimezone(ist)
                
                # Get the current time in IST
                current_time = timezone.now().astimezone(ist)
                
                # Debugging: Print current time and pickup time
                print(f"Current time (IST): {current_time}")
                print(f"Pickup time (IST): {pickup_datetime}")

                if pickup_datetime < current_time:
                    error_message = "Pickup time cannot be in the past."
                    return render(request, 'vehicledetails.html', {'bike': bike, 'message': error_message})
                
                end_datetime = pickup_datetime + timedelta(hours=hours)
                
                # Convert end_datetime to UTC for database consistency
                end_datetime_ist = end_datetime.astimezone(ist)
                
                # Debugging: Print end time
                print(f"End time (IST): {end_datetime}")
                
            except ValueError:
                return HttpResponse("Invalid pickup time format.")
        else:
            return HttpResponse("Pickup time is required.")
        
        # Check for overlapping rentals
        overlapping_rentals = Rental.objects.filter(
            bike=bike,
            start_time__lt=end_datetime_ist,
            end_time__gt=pickup_datetime_ist
        )
        
        if overlapping_rentals.exists():
            error_message = "The bike is already rented for the selected time period."
            return render(request, 'vehicledetails.html', {'bike': bike, 'message': error_message})
        
        hourly_rate = bike.hourly_rate
        total_cost = hours * hourly_rate
        
        rental, created = Rental.objects.update_or_create(
            bike=bike,
            user=request.user,
            defaults={
                'start_time': pickup_datetime_ist,
                'end_time': end_datetime_ist,
                'hour': hours,
                'total_cost': total_cost
            }
        )
        
        return redirect('vehicledetails', rid=bike_id)

    else:
        return HttpResponse("Invalid request method.")


@login_required(login_url="/login")
def vehicledetails(request, rid):
    if request.method == 'GET':
        bike = Bike.objects.filter(bike_id=rid).first()
        if bike:
            documents = Document.objects.filter(bike=bike, user=request.user)
            rental = Rental.objects.filter(bike=bike, user=request.user).order_by('-start_time').first()
            booking = Booking.objects.filter(bike=bike, user=request.user).first()
            
            formatted_start_time = ""
            message = ""
            if rental:
                
                ist = pytz.timezone('Asia/Kolkata')
                start_time_ist = localtime(rental.start_time, ist)
                end_time_ist = localtime(rental.end_time, ist)
                formatted_start_time = start_time_ist.strftime('%Y-%m-%dT%H:%M')
                
                # Check if the booking is active
                current_time_ist = localtime(timezone.now(), ist)
                
                print(f"rental.end_time time (IST): {end_time_ist}")
                print(f"timezone.now() (IST): {current_time_ist}")
                
                if booking and end_time_ist > current_time_ist:
                    message = "You already have an active booking for this bike."
            
            context = {
                'bike': bike,
                'documents': documents,
                'bike_id': bike.bike_id,
                'rent': rental,
                'formatted_start_time': formatted_start_time,
                'message': message,
                
            }
            return render(request, 'vehicledetails.html', context)
        else:
            return HttpResponse("Bike not found.")
    return HttpResponse("Invalid request method.")

@login_required
def book_now(request, rid):
    document_exists = Document.objects.filter(bike_id=rid, user=request.user).exists()
    
    if document_exists:
        if request.method == "POST":
            bike = Bike.objects.get(bike_id=rid)
            rental = Rental.objects.filter(user=request.user).first()
            
            if rental:
                
                ist = pytz.timezone('Asia/Kolkata')
                start_time_ist = localtime(rental.start_time, ist)
                end_time_ist = localtime(rental.end_time, ist)
                formatted_start_time = start_time_ist.strftime('%Y-%m-%d %H:%M')
                formatted_end_time = end_time_ist.strftime('%Y-%m-%d %H:%M')
                
                # Check if the booking is active
                current_time_ist = localtime(timezone.now(), ist)
                
                print(f"pyment end_time time (IST): {formatted_end_time}")
                print(f"pyment start time (IST): {start_time_ist}")
            
            
            
            is_available = request.POST.get('is_available') == 'True'
            
            if is_available:
                booking = Booking.objects.create(
                    user=request.user,
                    bike=bike,
                    rental=rental,
                    start_time=rental.start_time,
                    end_time=rental.end_time,
                    total_cost=rental.total_cost,
                )
                booking.save()
                
                context = {
                'bike': bike,
                'rental': rental,
                'formatted_start_time':formatted_start_time,
                'formatted_end_time': formatted_end_time 
                
            }
                                
                
                return render(request, 'payment.html', context)
            else:
                return HttpResponse("Bike is not available for booking.")
        
    else:
        return HttpResponse("Please upload documents.")


@login_required(login_url="/login")
def process_payment(request, rental_id):
    rental = Rental.objects.filter(id=rental_id, user=request.user).first()

    if not rental:
        message = "Rental not found."
        return render(request, 'index.html', {'message': message})

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'make_payment':
            # Handle the payment logic here
            message = "Vehicle is booked."
            return render(request, 'payment_success.html', {'message': message})

        elif action == 'cancel':
            # Cancel the booking and delete the rental record
            booking = Booking.objects.filter(rental=rental).first()
            if booking:
                booking.delete()
            rental.delete()
            message = "Booking has been cancelled."
            return render(request, 'booking_cancelled.html', {'message': message})

    # If the request method is not POST or the action is not recognized
    message = "Invalid request."
    return render(request, 'index.html', {'message': message})  

    
    
def create_review(request, rid):
    
    bike = Bike.objects.get(bike_id=rid)
    rev = Review.objects.filter(bike_id = bike, user=request.user).first()
    
    
    if rev:
        return HttpResponse('Review Already added')
    else:
        if request.method == "GET":
            return render(request, 'create_review.html')
        else:
            title = request.POST.get('title')
            content = request.POST.get('content')
            rating = request.POST.get('rate')
            image = request.FILES.get('image')
            
            review = Review.objects.create(bike=bike, user=request.user, title=title, content=content, rating=rating, image=image)
            review.save()
            return HttpResponse("Review Saved")





def mybooking(request):
    if request.method == "GET":
        book = Booking.objects.filter(user_id=request.user)
        us = request.user
        
        context = {
            'bookis': book,
            'user': us
        }

        return render(request, 'mybooking.html', context)
    
    
def profile_view(request):
    
    if request.method == "GET":
        
        users = request.user
        
        context = {}
        
        context['user'] = users
        
        return render(request, 'profile.html', context)
    
    return render(request, 'profile.html')

@login_required
def settings_view(request):
    if request.method == 'POST':
        # Update user profile
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username:
            request.user.username = username
        if email:
            request.user.email = email
        if password:
            request.user.set_password(password)
            update_session_auth_hash(request, request.user)  # Keep the user logged in after password change
        request.user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('settings')

    return render(request, 'settings.html')    

   
    
        
                
        
            
       