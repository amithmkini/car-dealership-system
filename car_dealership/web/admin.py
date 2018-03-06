from django.contrib import admin
from .models import Car, TestDrive, Order

# Register your models here.
admin.site.register(Car)
admin.site.register(TestDrive)
admin.site.register(Order)
