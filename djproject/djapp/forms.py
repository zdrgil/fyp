from django import forms
from .models import *
from django.contrib.auth.forms import PasswordChangeForm

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'doctor', 'customer', 'clinic', 'fullname', 'sex', 'age']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }



class EditappointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['id', 'date', 'time', 'doctor', 'fullname', 'sex', 'age','state']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'id': forms.HiddenInput(),
        }



class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['id','fullname' , 'sex', 'age', 'phonenumber']
        widgets = {
   
            'id': forms.HiddenInput(),
        }       

class EditAdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['id','fullname']
        widgets = {
   
            'id': forms.HiddenInput(),
        }

class EditDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['id','name','state']
        widgets = {
   
            'id': forms.HiddenInput(),
        }


from django.contrib.auth.forms import UserCreationForm

class AddAdminUserForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        return user
    

class AddDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'sex']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
           
        }


class EditClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['clinicname', 'location', 'telnum', 'state']

         

        
class AddappointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'doctor', 'fullname', 'sex', 'age', 'state', 'clinic']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = kwargs['initial']['user']
        if hasattr(user, 'superadmin'):
            clinic = user.superadmin.clinic
            self.fields['doctor'].queryset = Doctor.objects.filter(clinic=clinic)
            self.fields['clinic'].initial = clinic
            self.fields['clinic'].widget = forms.HiddenInput()
        elif hasattr(user, 'admin'):
            clinic = user.admin.clinic
            self.fields['doctor'].queryset = Doctor.objects.filter(clinic=clinic)
            self.fields['clinic'].initial = clinic
            self.fields['clinic'].widget = forms.HiddenInput()
        else:
            self.fields['doctor'].queryset = Doctor.objects.none()
            self.fields['clinic'].queryset = Clinic.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get("doctor")
        clinic = cleaned_data.get("clinic")
        if doctor and clinic and doctor.clinic != clinic:
            raise forms.ValidationError(
                "The selected doctor does not belong to the selected clinic."
            )
        

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.HiddenInput(), initial='')

    def clean_old_password(self):
        return self.cleaned_data['old_password']     