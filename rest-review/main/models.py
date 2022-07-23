from django.db import models

# Create your models here.

class Rest(models.Model):
    user = models.CharField(max_length=255, db_index=True)
    restaraunt = models.CharField(max_length=255)
    rating = models.DecimalField(decimal_places=1,max_digits=2) 	
    category = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=50)
    drive_time = models.IntegerField()
    notes = models.TextField()
