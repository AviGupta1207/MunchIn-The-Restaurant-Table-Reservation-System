from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import datetime



# User._meta.get_field('email')._unique = True
# Create your models here.

# #SAMPLE EXAMPLE                          
# class Student(models.Model):                      CREATE TABLE "enroll_student"(
#     stuid = models.IntegerField()                      "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, #Created by Django ORM
#     stuname = models.CharField(max_length=50)          "stuid" integer NOT NULL,                   
#     stuemail = models.CharField(max_length=50)         "stuname" varchar(50) NOT NULL,   
#     stuphone = models.CharField(max_length=10)         "stuphone" varchar(10) NOT NULL  
                                                            #);    

#Creating Models for Book-A-Table

table_choices = [ ('single','Single/Couple Table (1 to 2 Members)'),('small','Small Family Table (2 to 4 Members)'),('mini','Mini-Joint Family Table (4-6 Members)'),('jointf','Joint Family Table (6-12 Members)')]

time_choices = [('1','7:00PM'),('2','7:30 PM'),('3','8:00PM'),('4','8:30PM'),('5','9:00PM'),('6','9:30PM'),('7','10:00PM'),('8','10:30 PM'),('9','11:00 PM')]



class Booking(models.Model):
    uname = models.CharField(max_length=30)
    phone_regex = RegexValidator(regex=r'^[6-9]\d{9}$')
    uphone = models.CharField(validators=[phone_regex],max_length=10)
    utable = models.CharField(max_length=50,choices=table_choices)
    uarrtime = models.CharField(max_length=50,choices=time_choices)
    umsg = models.TextField(max_length=500,default='No Messages')
    CheckIn = models.BooleanField(default=False)
    CheckOut = models.BooleanField(default=False)



# Model For OTP
class UserOTP(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    time_st = models.DateTimeField(auto_now = True)
    # otp = models.SmallIntegerField()
    otp = models.CharField(max_length=6)

class FoodItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=300,default='')
    image = models.ImageField(upload_to='munchin/static/FoodItem/')

    @staticmethod
    def get_fooditems_by_id(ids):
        return FoodItem.objects.filter(id__in=ids)

    @staticmethod
    def get_all_fooditems():
        return FoodItem.objects.all()

class Foodorder(models.Model):
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=200,default='',blank=True)
    phone = models.CharField(max_length=10,default='',blank=True)
    debitcard = models.CharField(max_length=16,default='')
    expiry = models.CharField(max_length=5,default='')
    cvv = models.CharField(max_length=3,default='')
    date = models.DateTimeField(default=datetime.datetime.today)
    Completed = models.BooleanField(default=False)

    @staticmethod
    def placeOrder(self):
        return self.save()

    @staticmethod
    def get_orders_by_user(user_id):
        return Foodorder.objects.filter(user=user_id)










#After Creating above class open terminal and type 
# 1. python manage.py makemigrations (It will create the queries for above defined class and if there are changes it make migrations)
# 2.python manage.py migrate (It will execute the queries created above)

#!3. sqlmigrate(Displays SQL statements for migrations) #Syntax : python manage.py sqlmigrate enroll(application_name) 0001(dbfile_name)
# 4.showmigrations(Lists a project's migrations and their status)