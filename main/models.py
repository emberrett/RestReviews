from django.db import models

# Create your models here.


class Rest(models.Model):
    user = models.CharField(max_length=255, db_index=True)
    rest = models.CharField(max_length=255)
    rating = models.DecimalField(decimal_places=1, max_digits=2,default=None,null=True)
    my_rating = models.DecimalField(decimal_places=1, max_digits=2,default=None,null=True)
    address = models.TextField(default=None,null=True)
    category = models.CharField(max_length=255,default=None,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,default=None,null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,default=None,null=True)
    notes = models.TextField(default=None,null=True)
