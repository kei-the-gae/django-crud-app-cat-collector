from django.db import models
# Import the reverse function
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Tuple of 2-tuples to represent meal times
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.
# Many-to-many relationships:
class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toy-detail', kwargs={'pk': self.id})

class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    # Add the M:M relationship
    toys = models.ManyToManyField(Toy)
    # Add the foreign key linking to a user instance
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Good practice: override the __str__ method in a model so they print in a more helpful way
    def __str__(self):
        return self.name

# Define a method to get the URL for this particular cat instance
    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this cat's details
        return reverse('cat-detail', kwargs={'cat_id': self.id})

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

# One-to-many relationship:
class Feeding(models.Model):
    date = models.DateField('Feeding date')
    meal = models.CharField(
        max_length=1,
        # Defining choices for Field.choice dropdown
        choices=MEALS,
        default=MEALS[0][0]
    )
    # Create a cat_id column for each feeding in the database
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f'{self.get_meal_display()} on {self.date}'

    # Define the default order of feedings
    class Meta:
        ordering = ['-date']  # This line makes the newest feedings appear first
