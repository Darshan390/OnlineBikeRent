
class Donor(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), 
        ('B+', 'B+'), ('B-', 'B-'), 
        ('AB+', 'AB+'), ('AB-', 'AB-'), 
        ('O+', 'O+'), ('O-', 'O-')
    ]
    
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    mobile_no = models.BigIntegerField()
    quantity = models.IntegerField()
    bloodgroup = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    disease = models.CharField(max_length=200, blank=True, null=True)
    age = models.IntegerField()
    
    
class Patient(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    p_name = models.CharField(max_length=200)
    p_address = models.CharField(max_length=200)
    p_mobile = models.BigIntegerField()
    quantity = models.IntegerField()
    p_disease = models.CharField(max_length=200, blank=True, null=True)
    p_age = models.IntegerField()
    date = models.DateField(default=lambda: datetime.now().strftime('%Y-%m-%d'))  # Example field addition
