from django.urls import path
from . import views
from .views import   AddDoctorView, AppointmentByCustomerAPIView, AppointmentCreateView, AppointmentViewSet, ChatLogAPIView, ChatLogViewSet, ClinicListAPIView, ClinicViewSet, CurrentUserIDAPIView, DoctorListAPIView, DoctorViewSet, EditAdminView, EditAppointmentView, EditClinicView, EditCustomerView,AddAppointmentView, EditDoctorView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.contrib.auth.models import User
from rest_framework import routers
from .views import UserViewSet,GetCSRFToken,RegisterUserAPIView,LoginAPIView,LogoutAPIView
from rest_framework.authtoken.views import obtain_auth_token



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clinics', ClinicViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'chatlogs', ChatLogViewSet)
router.register(r'doctors', DoctorViewSet)





urlpatterns = [
    path('', views.index,name='index'),
    path('Registration', views.Registration,name='Registration'),
    path('Loginpage', views.Loginpage,name='Loginpage'),
    path('Logout', views.Logout,name='Logout'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('adminpage/<str:username>/', views.adminpage, name='adminpage'),
    path('adminpage/<str:username>/customerlist/', views.Customerlist,name='customerlist'),
    path('change-password/<int:customer_id>/', views.ChangePasswordView.as_view(), name='change_password'),
    path('adminpage/<str:username>/Appointmentlist/', views.Appointmentlist,name='Appointmentlist'),
    path('edit_appointment/<int:pk>/', EditAppointmentView.as_view(), name='edit_appointment'),
    path('edit_customer/<int:pk>/', EditCustomerView.as_view(), name='edit_customer'),    
    path('edit_admin/<int:pk>/', EditAdminView.as_view(), name='edit_admin'),
    path('edit_doctor/<int:pk>/', EditDoctorView.as_view(), name='edit_doctor'),
    path('edit_clinic/<int:pk>/', EditClinicView.as_view(), name='edit_clinic'),
    path('add_appointment/', AddAppointmentView.as_view(), name='add_appointment'),
    path('add_doctor/', AddDoctorView.as_view(), name='add_doctor'),
    path('register_admin/', views.register_admin, name='register_admin'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('delete_admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),
    path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('adminlogin', views.adminlogin, name='adminlogin'),
    path('adminregistration', views.adminregistration, name='adminregistration'),
    path('adminLogout', views.adminLogout,name='adminLogout'),
    path('chatbot', views.chatbot,name='chatbot'),
    path('adminpage/adminlist/<str:username>/', views.adminlist,name='adminlist'),
    path('adminpage/doctorlist/<str:username>/', views.doctorlist,name='doctorlist'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/login/', LoginAPIView.as_view(), name='login_logout'),
    path('api/logout/', LogoutAPIView.as_view(), name='login_logout'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/get_csrf_token/', GetCSRFToken.as_view(), name='get_csrf_token'),
    path('users/current_user/', UserViewSet.as_view({'get': 'get_current_user'}), name='current-user'),
    path('api/register_user/', RegisterUserAPIView.as_view(), name='register_user'),
    path('api/clinics/',ClinicListAPIView.as_view() , name='clinics'),
    path('api/register_appointment/', AppointmentCreateView.as_view(), name='register_appointment'),
    path('api/chatlog/', ChatLogAPIView.as_view(), name='chatlog'),
    path('api/rasagetuser/', CurrentUserIDAPIView.as_view(), name='rasagetuser'),
    path('api/doctors/', DoctorListAPIView.as_view(), name='doctors'),
    path('api/appointments/customer/<int:customer_id>/', AppointmentByCustomerAPIView.as_view()),







]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)