from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name