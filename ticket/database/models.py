from typing import Iterable, Optional
from django.db import models
from django.utils.text import slugify 
from datetime import *
import datetime
# Create your models here.
class Dates(models.Model):
    date = models.DateField()
    def __str__(self) -> str:
        return f"{self.date}"

class Times(models.Model):
    time = models.TimeField()
    def __str__(self):
        return f"{self.time}"

class Demo(models.Model):
    name = models.CharField(max_length=50)
    certificate =models.CharField(max_length=5)
    aval_lan = models.CharField(max_length=20)
    img = models.ImageField(upload_to="uploads/Demo/")
    slug = models.SlugField(default="")

    def __str__(self) -> str:
        return f"{self.name} {self.aval_lan}"
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class UserData(models.Model):
    name = models.CharField(max_length=50)  
    email = models.EmailField(max_length=254)
    create_at = models.DateField(auto_now=True) 

    def __str__(self) -> str:
        return f"{self.name} {self.email}"
    
class Booked(models.Model):
    movie = models.ForeignKey(Demo,on_delete=models.CASCADE)
    date = models.ForeignKey(Dates,on_delete=models.CASCADE)
    time =models.ForeignKey(Times,on_delete=models.CASCADE)
    seats_index =models.CharField(max_length=500)

    def __str__(self) -> str:
        return f"{self.movie}--{self.date}--{self.time}--{self.seats_index}"
