from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError



class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']
        labels = {'email':'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True, 'class': 'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'autofocus':True, 'class': 'form-control'}), help_text= password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}))



class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocompplete': 'new-password', 'class': 'form-control'})
    )


class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        fields = ["subject", "title", "description", "due_date", "completed"]
        widgets = {'subject': forms.TextInput(attrs={'class':'form_control'}),
                'title':forms.TextInput(attrs={'class':'form_control'}) ,
                'description': forms.Textarea(attrs={'class':'form_control'}),
                "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["title", "description"]
        widgets = {'title':forms.TextInput(attrs={'class':'form_control'}),
                'description':forms.Textarea(attrs={'class':'form_control'})
                }

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Search")


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ["title", "finished"]
        widgets = {'title':forms.TextInput(attrs={'class':'form_control'}),
                }
        
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['reg_no', 'cls', 'full_name', 'phone', 'img']
        widgets = { 'reg_no':forms.TextInput(attrs={'class':'form_control'}),
                'cls':forms.Select(attrs={'class':'form_control'}),
                'full_name ':forms.TextInput(attrs={'class':'form_control'}),
                'phone':forms.NumberInput(attrs={'class':'form_control'}),
                
        }
    img = forms.ImageField(required=False) 


class LectureProfileForm(forms.ModelForm):
    class Meta:
        model = LectureProfile
        fields = ['full_name', 'department', 'phone', 'img']
        widgets = {
            'full_name':forms.TextInput(attrs={'class':'form_control'}),
            'department': forms.Select(attrs={'class':'form_control'}),
            'phone':forms.TextInput(attrs={'class':'form_control'}),
        }
    img = forms.ImageField(required=False)

# class AssignmentForm(forms.ModelForm):
#     class Meta:
#         model = Assignments
        
#         fields = ["lecture", "title", "description", "document"]
#         widgets = {'lecture':forms.TextInput(attrs={'class':'form_control'}),
#                 'title':forms.TextInput(attrs={'class':'form_control'}),
#                 'description':forms.TextInput(attrs={'class':'form_control'}),

#                 }
#     document = forms.FileField(required=False) 


class AssignmentForm(forms.ModelForm):
    lecture = forms.ModelChoiceField(
        queryset=LectureProfile.objects.all(),  # Query to fetch all lecture profiles
        empty_label=None,  # Prevent an empty option in the dropdown
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Assignments
        fields = ["lecture", "title", "description", "document"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    document = forms.FileField(required=False)


    
class LectureAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignments
        fields = ["document", "valued"]
        