from django.contrib import admin

# Register your models here.
from FamilyLogin.models import FamilyMembers,Expenses

admin.site.register(FamilyMembers)
admin.site.register(Expenses)
