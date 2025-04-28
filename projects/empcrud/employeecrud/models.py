from django.db import models

# Create your models here.

from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    designation = models.CharField(max_length=50)

    def __str__(self):
        return self.name
