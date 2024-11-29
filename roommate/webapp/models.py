from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

# Create your models here.
class User_detail(models.Model):
    user_id = models.CharField(max_length=12, unique=True, primary_key=True)   
    username=models.ForeignKey( User, on_delete=models.CASCADE,default=None)
    first_name = models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    phone = models.IntegerField()
    address= models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, blank=True) #Male/Female
    date_of_birth= models.DateField( blank=True,null=True)
    
    
    def __str__(self):
        return "User ID: "+ self.user_id + " -----------------------  " + "Name: " + self.first_name +" "+ self.last_name 

class Post(models.Model):
    # Choices for fields with predefined options
    DURATION_CHOICES = [
        (1, "2 Weeks"),
        (2, "3 Weeks"),
        (3, "1 Month"),
        (4, "2 Months"),
    ]

    SECURITY_DEPOSIT_CHOICES = [
        ("No Deposit", "No Deposit"),
        ("Half Month Rent", "Half Month Rent"),
        ("1 Month Rent", "1 Month Rent"),
        ("2 Months Rent", "2 Months Rent"),
    ]

    LEASE_TERM_CHOICES = [
        ("No Lease", "No Lease"),
        ("4 Months", "4 Months"),
        ("6 Months", "6 Months"),
        ("1 Year", "1 Year"),
        ("2 Years", "2 Years"),
        ("Other", "Other"),
    ]

    # Model fields
    post_id = models.CharField(max_length=20, unique=True, primary_key=True)
    duration = models.IntegerField(choices=DURATION_CHOICES, default=4)
    tenant_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    bed = models.CharField(max_length=100)
    resident_type = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    rent = models.PositiveIntegerField()
    area = models.PositiveIntegerField(null=True, blank=True)  # Optional
    furnished = models.CharField(max_length=100)
    security_deposit = models.CharField(max_length=50, choices=SECURITY_DEPOSIT_CHOICES, default="No Deposit")
    lease_term = models.CharField(max_length=50, choices=LEASE_TERM_CHOICES, default="No Lease")
    utilities_included = models.JSONField(default=list, blank=True)  # List of selected utilities
    non_included_bills = models.JSONField(default=list, blank=True)  # List of selected non-included bills
    image1 = models.ImageField(null=True, blank= True, upload_to='post/')
    image2 = models.ImageField(null=True, blank= True, upload_to='post/')
    image3 = models.ImageField(null=True, blank= True, upload_to='post/')
    image4 = models.ImageField(null=True, blank= True, upload_to='post/')
    
    entry_date = models.DateField(auto_now_add=True)
    
    #needs updating
    '''created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        # Set `expires_at` based on `duration` when saving
        if not self.expires_at:
            duration_mapping = {
                1: 14,  # 2 Weeks
                2: 21,  # 3 Weeks
                3: 30,  # 1 Month
                4: 60,  # 2 Months
            }
            self.expires_at = now() + timedelta(days=duration_mapping.get(self.duration, 60))
        super().save(*args, **kwargs)'''
 
class Favorites(models.Model):
    
    SECURITY_DEPOSIT_CHOICES = [
        ("No Deposit", "No Deposit"),
        ("Half Month Rent", "Half Month Rent"),
        ("1 Month Rent", "1 Month Rent"),
        ("2 Months Rent", "2 Months Rent"),
    ]

    LEASE_TERM_CHOICES = [
        ("No Lease", "No Lease"),
        ("4 Months", "4 Months"),
        ("6 Months", "6 Months"),
        ("1 Year", "1 Year"),
        ("2 Years", "2 Years"),
        ("Other", "Other"),
    ]
    
    username=models.ForeignKey( User, on_delete=models.CASCADE,default=None)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE,default=None)
    tenant_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    bed = models.CharField(max_length=100)
    resident_type = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    rent = models.PositiveIntegerField()
    area = models.PositiveIntegerField(null=True, blank=True)  # Optional
    furnished = models.CharField(max_length=100)
    security_deposit = models.CharField(max_length=50, choices=SECURITY_DEPOSIT_CHOICES, default="No Deposit")
    lease_term = models.CharField(max_length=50, choices=LEASE_TERM_CHOICES, default="No Lease")
    utilities_included = models.JSONField(default=list, blank=True)  # List of selected utilities
    non_included_bills = models.JSONField(default=list, blank=True)  # List of selected non-included bills
    image1 = models.ImageField(null=True, blank= True, upload_to='post/')
    
    def __str__(self):
        return f"Fav ID: {self.username}"  # Use `username` instead of `user_name`
    