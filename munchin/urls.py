#I have created these urls.py file.
#We are defining our url patterns for our views.py in these file.
from django.contrib import admin
from django.urls import path,include  #me #me
from django.contrib.auth import views as auth_views
from munchin import views#Importing Views
from .views import *

urlpatterns = [
    path('',views.index,name='index'), 
    path('book/',views.book,name='book'),
    path('signup/',views.user_signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('accounts/login/', auth_views.LoginView.as_view()),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.user_profile,name='profile'),
    path('changepassword/',views.user_change_pass,name='changepass'),

    #Reset Password Using Mail    
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="Enroll/reset_password.html"),name='forgetpass'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="Enroll/reset_password_sent.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="Enroll/reset_password_confirm.html"),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="Enroll/reset_password_complete.html"),name='password_reset_complete'),

   #Cart ---------------------------------------------------------------------------------------
    path('foodmenu/',Foodmenu.as_view(),name="foodmenu"),
    path('foodcart/',Foodcart.as_view(),name="foodcart"),
    path('checkout/',Foodcheckout.as_view(),name="checkout"),
    path('orders/',Order.as_view(),name="orders"),
    path('payment/',views.user_payment,name="payment")

]


#Now we will include these urls.py(application folder) file inside urls.py(Project folder).
