from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from jsonschema import ValidationError
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class Region(models.Model):
    name = models.CharField(max_length=30, null=True)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    SEX_CHOICES = (
        ('male', 'Male'), ('female', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=30, null=True)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)])
    sex = models.CharField(max_length=10, null=True, choices=SEX_CHOICES)
    phonenumber = models.CharField(max_length=20, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    login_status = models.BooleanField(default=False)

    @property
    def encrypted_password(self):
        return self.user.password

    def set_password(self, new_password):
        self.user.set_password(new_password)
        self.user.save()

    def __str__(self):
        return self.fullname
    


class Clinic(models.Model):
    STATUS_CHOICES = (
        ('open', 'open'), ('close', 'close'),
    )

    clinicname = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    telnum = models.CharField(max_length=12, blank=True, null=True)
    state = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='close')
    superadmin = models.OneToOneField(
        'SuperAdmin', on_delete=models.CASCADE, related_name='superadmin_clinic', null=True, blank=True)

    def __str__(self):
        return self.clinicname


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=30, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name='admins', null=True)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname

    class Meta:
        permissions = [
            ("can_manage_customer", "Can manage customer"),
            ("can_manage_doctor", "Can manage doctor"),
            ("can_manage_appointment", "Can manage appointment"),
        ]


class SuperAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=30, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name='clinic_superadmin', null=True)

    def __str__(self):
        return f"{self.clinic.clinicname} with Superadmin-{self.fullname}"

    class Meta:
        permissions = [
            ("can_manage_clinic", "Can manage clinic"),
            ("can_manage_admin", "Can manage admin"),
            ("can_manage_doctor", "Can manage doctor"),
            ("can_manage_customer", "Can manage customer"),
            ("can_manage_appointment", "Can manage appointment"),
        ]


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    try:
        SuperAdmin.objects.get(user=instance)
        raise models.ProtectedError(
            'Cannot delete user with SuperAdmin records', user_pre_delete)
    except SuperAdmin.DoesNotExist:
        pass


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected'),
    )
    SEX_CHOICES = (
        ('male', 'Male'), ('female', 'Female'),
    )

    date = models.DateField()
    time = models.TimeField()
    doctor = models.ForeignKey(
        'Doctor', on_delete=models.CASCADE, limit_choices_to={'state': 'onduty'})
    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=30, null=True)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)], null=True)
    sex = models.CharField(max_length=10, null=True, choices=SEX_CHOICES)
    state = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    clinic = models.ForeignKey(
        Clinic, null=True, on_delete=models.CASCADE,
        limit_choices_to={'state': 'open'}
    )

    def __str__(self):
        return f"{self.doctor.name}'s appointment with {self.fullname} on {self.date} at {self.time} at {self.clinic.clinicname}"

    def clean(self):
        if self.doctor.clinic != self.clinic:
            raise ValidationError('Doctor and clinic do not match.')


    @staticmethod
    def get_appointment_by_id(appointment_id):
        try:
            return Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return None       


class Doctor(models.Model):
    SEX_CHOICES = (
        ('Male', 'Male'), ('Female', 'Female'),
    )

    name = models.CharField(max_length=30, null=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    clinic = models.ForeignKey( 
        Clinic, on_delete=models.CASCADE, related_name='doctors',null=True)
    STATUS_CHOICES = (
        ('onduty', 'onduty'), ('offduty', 'offduty'),
    )

    state = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='offduty')

    def __str__(self):
        return self.name
    

class ChatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    sender = models.TextField(null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatLog: {self.message}"
    
