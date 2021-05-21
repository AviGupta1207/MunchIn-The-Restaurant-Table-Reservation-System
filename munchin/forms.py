from django import forms
from .models import Booking,table_choices,time_choices
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm,PasswordChangeForm,UsernameField
from django.core.validators import RegexValidator
from django.utils.translation import gettext, gettext_lazy as _
from django.forms.fields import ChoiceField

class UserBooking(forms.ModelForm):
    name_regex = RegexValidator(regex='^[a-zA-z]*$',message='Name must contain alphabats only',code='invalid_uname')
    uname = forms.CharField(max_length=30,label="Full Name",widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter Full Name'}))
    uphone = forms.CharField(label='Phone Number',widget=forms.NumberInput(attrs={'class':'form-control form-control-sm','placeholder':'Enter Phone Number'}))
    umsg = forms.CharField(label='Any Special Request/Message',widget=forms.Textarea(attrs={'class':'form-control form-control-sm'}))
    utable = ChoiceField(label='Choose Table Type',choices=table_choices, widget=forms.Select(attrs={'class':'form-control form-control-sm','id':"exampleFormControlSelect1"}))
    uarrtime = ChoiceField(label='Choose Expexted Time Of Arrival',choices=time_choices, widget=forms.Select(attrs={'class':'form-control form-control-sm','id':"exampleFormControlSelect1"}))
    umsg = forms.CharField(max_length=500,label="Any Special Request/Messages (Type 'No' If No Message)",widget=forms.Textarea(attrs={'class': 'form-control form-control-sm','rows':'3'}))
    class Meta:
        model = Booking
        fields = ['uname','uphone','utable','uarrtime','umsg']
        labels = {'uname':'Full Name','uphone':'Phone Number','utable':'Choose Table Type','uarrtime':'Expected Time Of Arrival','umsg':'Any Special Request','CheckIn':'User Has Checked-In','CheckOut':'User Had Checked-Out'}   

class SignUpForm(UserCreationForm):
    name_regex = RegexValidator(regex='^[a-zA-Z]*$',message='Name must contain alphabats only',code='invalid_first_name')
    email_regex = RegexValidator(regex='^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$',message='Enter a valid email',code='invalid_email')
    email = forms.CharField(max_length=30,required=True,validators=[email_regex],widget=forms.TextInput(attrs={'class': 'form-control form-control-sm ','placeholder':'Enter Email Address'}))
    first_name = forms.CharField(max_length=30,required=True,validators=[name_regex],widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter First Name'}))
    last_name = forms.CharField(max_length=30,required=True,validators=[name_regex],widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter Last Name'}))
    password1 = forms.CharField(label='Enter Password',widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter Password'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm','placeholder':'Re-Type Password'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email':'Email Address'}
        widgets = {'username':forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter Username (Going To Be Used For Login)'}),
        'first_name':forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter First Name'}),
        'last_name':forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter Last Name'}),
        'email':forms.EmailInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter Email Address'})}
        # User._Meta.get_field_by_name('email').unique=True
     
        


class LoginForm(AuthenticationForm):
    # username = UsernameField(required=True,widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control form-control-sm'}))
    # password = forms.CharField(label=_('Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control form-control-sm'}))
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,'class': 'form-control form-control-sm'}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class': 'form-control form-control-sm'}),)
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }


class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email': 'Email'}
        widgets = {'username':forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter Username (Going To Be Used For Login)'}),
        'first_name':forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter First Name'}),
        'last_name':forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter Last Name'}),
        'email':forms.EmailInput(attrs={'class': 'form-control form-control-sm','placeholder':'Enter Email Address'})}

class EditAdminProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        exclude = ['groups','user_permissions']
        labels = {'email': 'Email'}

class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password :',widget=forms.PasswordInput(attrs={'autocomplete':'off','class': 'form-control form-control-sm','placeholder':'Enter Current Password'}))
    new_password1 = forms.CharField(label='New Password :',widget=forms.PasswordInput(attrs={'autocomplete':'off','class': 'form-control form-control-sm','placeholder':'Enter New Password'}))
    new_password2 = forms.CharField(label='Retype New Password :',widget=forms.PasswordInput(attrs={'autocomplete':'off','class': 'form-control form-control-sm','placeholder':'Enter New Password (again)'}))
    class Meta:
        model = User
        fields = '__all__'