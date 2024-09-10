from django.db import models

# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    
# Good practice: override the __str__ method in a model so they print in a more helpful way
    def __str__(self):
        return self.name
