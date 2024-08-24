from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BikeType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    
class Bike(models.Model):
    
    type_choices = (
        ('standard', 'Standard'),
        ('cruiser', 'Cruiser'),
        ('touring', 'Touring'),
        ('sports', 'Sports'),
        ('scooters', 'Scooters')
    )
    
    bike_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    bike_type = models.ForeignKey('BikeType', on_delete=models.CASCADE)
    category = models.CharField(max_length=200, choices=type_choices)
    is_available = models.BooleanField(default=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    original_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    deposit = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='image')
    location = models.CharField(max_length=200, null=True, blank=True)
    location_details = models.CharField(max_length=300, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    
    
class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    hour = models.IntegerField()
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
class Payment(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    
class Gallery(models.Model):
    
    image = models.ImageField(upload_to="gallery")
    
class Document(models.Model):
    
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='documents')
    user = models.ForeignKey(User, related_name='documents', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    adhar = models.FileField(upload_to='documents/adhar')
    driving_licence = models.FileField(upload_to='documents/licence')
    

class Booking(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)       
    

class Review(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField()
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)           
               
