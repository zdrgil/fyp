from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin
from django.forms import CheckboxSelectMultiple

class MemberInline(admin.TabularInline):
    model = Group.user_set.through
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

class MyGroupAdmin(GroupAdmin):
    inlines = [MemberInline]


admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)
admin.site.register(Customer)
admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Region)
admin.site.register(SuperAdmin)
admin.site.register(Admin)
admin.site.register(ChatLog)










