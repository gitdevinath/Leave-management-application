from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class addemployee(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password1 = models.CharField(max_length=12)
    password2 = models.CharField(max_length=12)

    def __str__(self) -> str:
        return self.username
    
CHOICES = (
    ('casual leave', 'Casual leave'), ('sick leave', 'Sick leave')
)

STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

class addLeave(models.Model):
    #employee = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length = 100)
    user_id = models.CharField(max_length=10)
    fromDate = models.DateTimeField()
    toDate = models.DateTimeField()
    reason = models.CharField(max_length=20, choices=CHOICES)
    comment = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


    def __str__(self):
        return self.username 
    

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    remaining_casual_leaves = models.IntegerField(default=12)
    remaining_sick_leaves = models.IntegerField(default=4)
    
    def __str__(self):
        return self.user.username

def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        profile.objects.create(user=instance)
    elif not instance.is_superuser:
        instance.profile.save()
   
