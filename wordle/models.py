from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  pass

class References(models.Model):
  referenceFrom= models.CharField(max_length=100)
  
  def __str__(self):
    return self.referenceFrom

class Posting(models.Model):
  title= models.CharField(max_length=250)
  writer= models.ForeignKey(User, on_delete=models.CASCADE, related_name="postWriter")
  words= models.CharField(max_length=1000)
  reference= models.ForeignKey(References, on_delete=models.CASCADE, related_name="postReference")

  def __str__(self):
    return self.writer

