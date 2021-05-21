from django.shortcuts import render,HttpResponseRedirect #pre
from .forms import UserBooking,SignUpForm,EditUserProfileForm,EditAdminProfileForm,LoginForm,UserChangePasswordForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random,string
from .models import UserOTP,FoodItem,Foodorder,User
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from django.utils.decorators import method_decorator

# from verify_email.email_handler import send_verification_email
# Create your views here.
# Creating views for munchin
# @login_required(login_url='/login/')
def index(request):
    print('You are:' , request.session.get('user_id'))
    return render(request,'Munch-In.html')

# @login_required(login_url='/login/')
def book(request):
        if request.user.is_authenticated:
            if request.method=="POST":
                fbd = UserBooking(request.POST)
                if fbd.is_valid():
                    fbd.save()
                    messages.success(request,'Table Booked Successfully!!,Choose Your Order')
                    return HttpResponseRedirect('/foodmenu/')
            else:
                fbd = UserBooking()
            return render(request,'Enroll/book-table.html',{'form':fbd})
        else:
            return HttpResponseRedirect('/login/')
#Signup Form

def user_signup(request):
    if request.method =="POST":
        get_otp = request.POST.get('otp')
        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username=get_usr)
            if get_otp == UserOTP.objects.filter(user = usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.success(request,'Verification Done!, Account Created Successfully!!')
                return HttpResponseRedirect('/login/')
            else:
                messages.warning(request,'You Have Entered a Wrong OTP')
                return render(request,'Enroll/signup.html',{'otp':True,'usr':usr})
        fsu = SignUpForm(request.POST)
        if fsu.is_valid():
            fsu.save()
            username = fsu.cleaned_data.get('username')
            email = fsu.cleaned_data.get('email')
            name = fsu.cleaned_data.get('first_name')
            usr = User.objects.get(username=username)
            usr.first_name = name
            usr.email = email
            usr.is_active = False
            usr.save()
            # usr_otp =random.randint(100000,999999)
            usr_otp= ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            UserOTP.objects.create(user = usr,otp = usr_otp)
            msg = f"Greetings From MunchIn,\nHello {usr.first_name},\n Your OTP is {usr_otp}\nThanks!!"

            send_mail(
                "Welcome To MunchIn - Verify Your Email",
                msg,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently= False
            )
            return render(request,'Enroll/signup.html',{'otp':True,'usr':usr})           
    else:
        fsu = SignUpForm()   
    return render(request,'Enroll/signup.html',{'form1':fsu})

#Login Form
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fl = LoginForm(request=request,data=request.POST)
            if fl.is_valid():
                lname = fl.cleaned_data['username']
                lpass = fl.cleaned_data['password']
                user = authenticate(username=lname,password=lpass)
                if user is not None:
                    login(request, user)
                    request.session['user_id'] = user.id
                    request.session['username'] = lname
                    messages.success(request,'Logged In Successfully !!')
                    return HttpResponseRedirect('/book/')
        else:
            fl = LoginForm()
        return render(request,'Enroll/login.html',{'form':fl})
    else:
        return HttpResponseRedirect('/book/')

#PROFILE
def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_superuser == True: 
                 fuc = EditAdminProfileForm(request.POST,instance=request.user)
            else:
                fuc = EditUserProfileForm(request.POST,instance=request.user)
            if fuc.is_valid():
                messages.success(request,'Profile Updated !!!')
                fuc.save()
        else:
            if request.user.is_superuser == True:
                fuc = EditAdminProfileForm(instance=request.user)
            else:
                fuc = EditUserProfileForm(instance=request.user)
        return render(request,'Enroll/profile.html',{'name': request.user.username,'form':fuc})
    else:
        return HttpResponseRedirect('/login/')

#Log Out
def user_logout(request):
    request.session.clear()
    logout(request)
    return HttpResponseRedirect('/')

#Change Password with old password  
def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fps = UserChangePasswordForm(user=request.user,data=request.POST)
            if fps.is_valid():
                fps.save()
                update_session_auth_hash(request,fps.user)
                messages.success(request,'Change Password Successfully !!')
                return HttpResponseRedirect('/logout/')
        else:        
            fps = UserChangePasswordForm(user=request.user)
        return render(request,'Enroll/changepass.html',{'form':fps})
    else:
        return HttpResponseRedirect('/login/')


#CART -----------------------------------------------------------------------------------------------

# class LoginRequiredMixin(object):
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class Foodmenu(View):
    def post(self,request):
        if request.user.is_authenticated:
            fooditem = request.POST.get('fooditem')
            remove = request.POST.get('remove')
            # print(fooditem)
            cart = request.session.get('cart')
            if cart:
                quantity = cart.get(fooditem)
                if quantity:
                    if remove:
                        if quantity <= 1:
                            cart.pop(fooditem)
                        else:
                            cart[fooditem] = quantity-1
                    else:
                        cart[fooditem] = quantity+1
                else:
                    cart[fooditem] = 1
            else:
                cart = {}
                cart[fooditem] = 1

            request.session['cart'] = cart
            messages.success(request,f"Dish-{fooditem} Added To Cart")
            # print('cart : ',request.session['cart'])
            return HttpResponseRedirect('/foodmenu/')
        else:
            return HttpResponseRedirect('/login/')


    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        
        fooditems = FoodItem.get_all_fooditems()
        return render(request,'Enroll/Cart/foodmenu.html',{'fooditems':fooditems})



class Foodcart(View):
    def get(self,request):
        ids = list(request.session.get('cart').keys())
        fooditems = FoodItem.get_fooditems_by_id(ids)
        return render(request,'Enroll/Cart/foodcart.html',{'fooditems':fooditems})


class Foodcheckout(View):
    def post(self,request):
        address = request.POST.get('Address')
        phone = request.POST.get('phone')
        # user = request.session.get('User')
        user = request.user.id
        cart = request.session.get('cart')
        fooditems = FoodItem.get_fooditems_by_id(list(cart.keys()))
        dishesname = FoodItem.get_all_fooditems()
        # print(address,phone,user,cart,fooditems)
        for fooditem in fooditems:
            # print(cart.get(fooditem.id))
            foodorder = Foodorder(user=User(id=user),fooditem=fooditem,price=fooditem.price,address = address,phone= phone,quantity=cart.get(str(fooditem.id)))
            foodorder.save()
        request.session['cart'] = {}
        messages.success(request,'Order Booked Successfully, Thanks For Using MunchIn')
        return HttpResponseRedirect('/')
    # return render(request,'Enroll/Cart/checkout.html')

class Order(View):
    def get(self,request):
        user = request.user.id
        orders = Foodorder.get_orders_by_user(user)
        print(orders)
        return render(request,'Enroll/Cart/orders.html',{'orders':orders})


def user_payment(request):
    return render(request,'Enroll/Cart/payment.html')












































# def showBookingdata(request):
#     un = ''
#     fbd = ''
#     if request.method=="POST":
#         fbd = UserBooking(request.POST)
#         if fbd.is_valid():
#            fbd.save()
#         return render(request,'Munch-In.html')
#     else:
#         fbd = UserBooking()
#     # return render(request,'Booking/Booking.html',{'form':fbd})
#     return render(request,'Munch-In.html',{'form':fbd})







#Now we will create a file urls.py inside our application folder and will define url patterns for above views 

#WRITING CODE TO GET DB DATA in views.py
#Create studetails.html inside templates/enroll
# from enroll.models import Student
# def studentinfo(request):
#     stud = Student.object.all()
#     return render(request,'enroll/studetails.html',{'stu':stud})

#GOTO templates/enroll/studetails.html
#!Press Enter, inside body write {{stud}}
#GOTO urls.py inside urlpatterns write path('stu/',views.studentinfo),
#Goto urls.py(project) and write urlpatterns