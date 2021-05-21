from django.contrib import admin
from .models import *
# Register your models here.

# @admin.register(Booking)    #Using Decorators
class BookingAdmin(admin.ModelAdmin):
    list_display = ('uname','utable','uarrtime')

admin.site.register(Booking,BookingAdmin)  #Normal

admin.site.register(UserOTP)


class FoodItemAdmin(admin.ModelAdmin):
  list_display = ('name','price','image')

admin.site.register(FoodItem,FoodItemAdmin)
  #Normal
class FoodorderAdmin(admin.ModelAdmin):
  list_display = ('fooditem','user','quantity')

admin.site.register(Foodorder,FoodorderAdmin)

