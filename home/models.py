from django.db import models
from django.db import models
from django.contrib.auth.models import User

class dpt(models.Model):
# Create your models here.
    department_name=models.CharField(max_length=100)
    dpt_description=models.TextField()
    
    def __str__(self):
        return self.department_name

class doctors(models.Model):
    doctor_name=models.CharField(max_length=100)
    doctor_specialization=models.CharField(max_length=100)
    doctor_image=models.ImageField(upload_to='doctor_images/',null=True,blank=True)
    department_name=models.ForeignKey(dpt,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.doctor_name
class book_appointment(models.Model):
    patient_name=models.CharField(max_length=100)
    patient_email=models.EmailField()
    patient_phone=models.CharField(max_length=15)
    doctor_name=models.ForeignKey(doctors,on_delete=models.CASCADE)
    booked_on=models.DateField()
    user = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='appointments'
)

    
    def __str__(self):
        return (f"{self.patient_name} - {self.doctor_name} - {self.booked_on}")



class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )
    address = models.TextField(blank=True)

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
