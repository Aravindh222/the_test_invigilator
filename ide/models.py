from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from django.contrib.auth.models import Group,User
import random
from datetime import datetime

class Time_Table1(models.Model):
    OPT1 = (('Request', 'Request'),
        ('Accept', 'Accept'),
        ('Rejected', 'Rejected'),)
    Faculty = models.ForeignKey(User, on_delete=models.CASCADE)
    class_room = models.CharField(max_length=10,blank=False)
    date = models.DateField(blank=False)
    start_slot = models.IntegerField(blank=True,validators=[MaxValueValidator(24), MinValueValidator(0)])
    end_slot = models.IntegerField(blank=True,validators=[MaxValueValidator(24), MinValueValidator(0)])
    exam_name = models.CharField(max_length=10,blank=False)
    request_status = models.CharField(max_length=20, choices=OPT1,blank=False)

class Faculty_Table(models.Model):
    Faculty=models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    slot1=models.CharField(max_length=20,blank=False)
    slot2=models.CharField(max_length=20,blank=False)
    slot3=models.CharField(max_length=20,blank=False)
    slot4=models.CharField(max_length=20,blank=False)
    slot5=models.CharField(max_length=20,blank=False)
    slot6=models.CharField(max_length=20,blank=False)
    slot7=models.CharField(max_length=20,blank=False)
    slot8=models.CharField(max_length=20,blank=False)







