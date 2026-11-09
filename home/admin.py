from django.contrib import admin

from .models import  book_appointment, doctors, dpt
admin.site.register(dpt)
admin.site.register(doctors)
admin.site.register(book_appointment)

# Register your models here.
