from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    manufacturer = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    date_of_manufacture = models.DateField()
    warranty_information = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name
