from aiohttp import request
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from django.views import View
from psycopg2 import IntegrityError
from .models import ChatLog, Doctor, Clinic, Customer, Appointment, SuperAdmin, Admin
from django.http import JsonResponse
import datetime
from django.urls import reverse
from .forms import AddAdminUserForm, AddDoctorForm, AppointmentForm, EditAdminForm, EditClinicForm, EditDoctorForm, EditappointmentForm, EditCustomerForm, AddappointmentForm, ChangePasswordForm
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import UpdateView, CreateView
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import FormView
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import logout
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.serializers import HyperlinkedModelSerializer, SerializerMethodField

def index(request):
    clinics = Clinic.objects.filter(state='open')
    customer_info = {}
    user_id = None  # 初始化用户ID为None

    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            customer_info['fullname'] = customer.fullname
            customer_info['age'] = customer.age
            customer_info['sex'] = customer.sex
            user_id = request.user.id
        except Customer.DoesNotExist:
            # Handle the case where the customer does not exist for the current user
            customer_info['fullname'] = ''
            customer_info['age'] = ''
            customer_info['sex'] = ''
        # If user is authenticated, set `customer` to the corresponding Customer object
        customer = Customer.objects.get(user=request.user)
    else:
        customer_info['fullname'] = ''
        customer_info['age'] = ''
        customer_info['sex'] = ''
        # If user is not authenticated, set `customer` to None
        customer = None
    now = datetime.datetime.now()
    current_date = now.date().isoformat()
    current_time = now.time().strftime('%H:%M')
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            doctor = form.cleaned_data['doctor']
            clinic = form.cleaned_data['clinic']
            fullname = form.cleaned_data['fullname']
            sex = form.cleaned_data['sex']
            age = form.cleaned_data['age']

            if Appointment.objects.filter(clinic=clinic, doctor=doctor, date=date, fullname=fullname, age=age).exists():
                messages.info(request, 'Appointment exists')
                return redirect(reverse('index'))
            else:
                appointment = Appointment.objects.create(
                    date=date, time=time, doctor=doctor, customer=customer, clinic=clinic, fullname=fullname, sex=sex, age=age)
                appointment.save()
                messages.info(request, 'Success')
                return redirect(reverse('index'))
        else:
            return render(request, 'index.html', {'clinics': clinics, 'customer_info': customer_info, 'current_date': current_date, 'current_time': current_time, 'form': form})
    else:
        form = AppointmentForm()
    return render(request, 'index.html', {'clinics': clinics, 'customer_info': customer_info, 'current_date': current_date, 'current_time': current_time, 'form': form,'user_id': user_id})


def doctor_list(request):
    clinic_id = request.GET.get('clinic_id')
    if clinic_id:
        doctors = Doctor.objects.filter(clinic__id=clinic_id, state='onduty')
        data = [{'id': doctor.id, 'name': doctor.name} for doctor in doctors]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


def Registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        fullname = request.POST['fullname']
        age = request.POST['age']
        sex = request.POST['sex']
        phonenumber = request.POST['phonenumber']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username exit')
                return redirect('Registration')
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email)
                user.save()
                customer = Customer.objects.create(
                    user=user, fullname=fullname, age=age, sex=sex, phonenumber=phonenumber)
                customer.save()
                messages.info(request, 'Success')

                return redirect('Loginpage')
        else:
            messages.info(request, 'password not the same')
            return redirect('Registration')
    else:
        return render(request, 'Registration.html')


def Loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'credentials invalid')
            return redirect('Loginpage')
    else:
        return render(request, 'Loginpage.html')
    
def chatbot(request):

        return render(request, 'chatbot.html')    


def adminregistration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        clinicreate = request.POST['clinicreate']

        if password == password2:
            if User.objects.filter(username=username).exists() and Clinic.objects.filter(clinicname=clinicreate).exists():
                messages.info(request, 'Username already exists')
                return redirect('adminregistration')

            else:
                user = User.objects.create_user(
                    username=username, password=password)
                # 将用户分配到Superadmin组中
                superadmin_group = Group.objects.get(name='Superadmin')
                user.groups.add(superadmin_group)

                clinic = Clinic.objects.create(
                    clinicname=clinicreate,
                )

                superadmin = SuperAdmin.objects.create(
                    user=user,
                    fullname=user.username,
                    clinic=clinic,
                )

                clinic.superadmin = superadmin
                clinic.save()

                messages.success(request, 'Registration successful')

                return redirect('adminlogin')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('adminregistration')
    else:
        return render(request, 'adminregistration.html')


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            # 檢查用戶是否是 admin 或 superadmin 組成員
            if user.groups.filter(name__in=['admin', 'Superadmin']).exists():
                login(request, user)
                if user.groups.filter(name='admin').exists():
                    return redirect(reverse('adminpage', kwargs={'username': username}))
                else:
                    return redirect(reverse('adminpage', kwargs={'username': username}))
            else:
                messages.error(
                    request, 'You are not authorized to access this page.')
                return redirect('adminlogin')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('adminlogin')
    else:
        return render(request, 'adminlogin.html')


def Logout(request):
    auth.logout(request)
    return redirect('/')


def adminLogout(request):
    auth.logout(request)
    return redirect('adminlogin')


def profile(request, username):
    # 確認用戶是否已登入
    if request.user.is_authenticated and request.user.username == username:
        # 獲取當前用戶的Customer對象
        customer = Customer.objects.get(user=request.user)
        # 獲取當前用戶的所有Appointment對象
        appointments = Appointment.objects.filter(customer=customer)
        # 將Customer和Appointment傳遞到模板中，並渲染HTML頁面
        return render(request, 'suss.html', {'customer': customer, 'appointments': appointments})
    # 如果用戶未登入，重定向到登入頁面
    else:
        return redirect('Loginpage')


def adminpage(request, username):
    if request.user.is_authenticated and request.user.username == username:
        user = request.user
        clinic, objects = get_clinic_and_objects(user)

        if clinic:
            page_obj = paginate(objects['appointments'], 5, request.GET.get('page'))
            customers = get_filtered_customers(user)  # Get filtered customers
        else:
            page_obj = None
            customers = None

        context = {
            'appointments': page_obj,
            'doctors': objects.get('doctors'),
            'admins': objects.get('admins'),
            'user': objects.get('user'),
            'customers': customers,  # Add customers to the context
            'clinic':clinic,
        }
        return render(request, 'adminpage.html', context)
    else:
        return render(request, 'adminlogin.html')


def get_clinic_and_objects(user):
    try:
        clinic = user.superadmin.clinic
        objects = {
            'appointments': Appointment.objects.filter(clinic=clinic, state__in=['pending']),
            'doctors': Doctor.objects.filter(clinic=clinic),
            'admins': Admin.objects.filter(clinic=clinic),
            'user': user.superadmin,
        }
    except SuperAdmin.DoesNotExist:
        try:
            clinic = user.admin.clinic
            objects = {
                'appointments': Appointment.objects.filter(clinic=clinic, state__in=['pending']),
                'doctors': Doctor.objects.filter(clinic=clinic),
                'admins': Admin.objects.filter(clinic=clinic),
                'user': user.admin,
            }
        except Admin.DoesNotExist:
            clinic = None
            objects = {}
    return clinic, objects


def paginate(objects, per_page, page_number):
    paginator = Paginator(objects, per_page)
    return paginator.get_page(page_number)


def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()
    return redirect('adminpage', username=request.user.username)

def delete_admin(request, admin_id):
    admin = Admin.objects.get(id=admin_id)
    admin.delete()
    return redirect('adminlist', username=request.user.username)

def delete_doctor(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    doctor.delete()
    return redirect('doctorlist', username=request.user.username)


def get_filtered_customers(user):
    customers = Customer.objects.all()
    clinic, objects = get_clinic_and_objects(user)
    if clinic:
        customers = customers.filter(appointment__clinic=clinic).distinct()
    return customers

def Customerlist(request, username):
    if request.user.is_authenticated and request.user.username == username:
        customers = get_filtered_customers(request.user)
        page_obj = paginate(customers, 20, request.GET.get('page'))
        context = {'customers': page_obj}
        return render(request, 'Customerlist.html', context)
    else:
        return render(request, 'adminlogin.html')

def Appointmentlist(request, username):
    if request.user.is_authenticated and request.user.username == username:
        clinic, objects = get_clinic_and_objects(request.user)
        if clinic:
            appointments = Appointment.objects.filter(clinic=clinic)
            page_obj = paginate(appointments, 20, request.GET.get('page'))
            context = {'appointments': page_obj}
            return render(request, 'Appointmentlist.html', context)
    else:
        return render(request, 'adminlogin.html')
    

def adminlist(request, username):
    if request.user.is_authenticated and request.user.username == username:
        clinic, objects = get_clinic_and_objects(request.user)  # 获取当前superadmin的clinic
        admins = objects.get('admins', None)
        page_obj = paginate(admins, 20, request.GET.get('page'))
        context = {'admins': page_obj, 'clinic': clinic}  # 将clinic传递给模板

        superadmin_group = Group.objects.get(name='Superadmin')
        # 检查用户是否属于 Superadmin 组
        if request.user.groups.filter(name=superadmin_group).exists():
            user_groups = [superadmin_group.name]
        else:
            user_groups = []

        context['user_groups'] = user_groups  # 将用户组权限信息传递给模板

        return render(request, 'adminlist.html', context)
    else:
        return render(request, 'adminlogin.html')
    
def doctorlist(request, username):
    if request.user.is_authenticated and request.user.username == username:
        clinic, objects = get_clinic_and_objects(request.user)
        doctors = objects.get('doctors', None)  # 从对象中获取医生数据
        page_obj = paginate(doctors, 20, request.GET.get('page'))
        context = {'doctors': page_obj, 'clinic': clinic}
        # 用户已认证且用户名匹配
        # 执行其他逻辑
        return render(request, 'doctorlist.html', context)
    else:
        # 用户未认证或用户名不匹配
        return render(request, 'adminlogin.html')



def register_admin(request):
    if request.method == 'POST':
        form = AddAdminUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            clinic, _ = get_clinic_and_objects(request.user)
            admin = Admin.objects.create(user=user, fullname=user.username, clinic=clinic)
            
            # 获取 admin 权限组
            admin_group = Group.objects.get(name='admin')
            # 将用户添加到 admin 权限组
            user.groups.add(admin_group)
            
            return redirect('adminlist', username=request.user.username)
    else:
        form = AddAdminUserForm()
    return render(request, 'register_admin.html', {'form': form})

    

class EditAdminView(UpdateView):
    model = Admin
    form_class = EditAdminForm
    template_name = 'edit_admin.html'

    def get_success_url(self):
        return reverse('adminlist', kwargs={'username': self.request.user.username})    
    

class EditClinicView(UpdateView):
    model = Clinic
    form_class = EditClinicForm
    template_name = 'edit_clinic.html'

    def get_success_url(self):
        return reverse('adminpage', kwargs={'username': self.request.user.username})        
    

class EditDoctorView(UpdateView):
    model = Doctor
    form_class = EditDoctorForm
    template_name = 'edit_doctor.html'

    def get_success_url(self):
        return reverse('doctorlist', kwargs={'username': self.request.user.username})    



class EditAppointmentView(UpdateView):
    model = Appointment
    form_class = EditappointmentForm
    template_name = 'edit_appointment.html'

    def get_success_url(self):
        return reverse('Appointmentlist', kwargs={'username': self.request.user.username})


class EditCustomerView(UpdateView):
    model = Customer
    form_class = EditCustomerForm
    template_name = 'edit_customer.html'

    def get_success_url(self):
        return reverse('customerlist', kwargs={'username': self.request.user.username})


class AddAppointmentView(CreateView):
    model = Appointment
    form_class = AddappointmentForm
    template_name = 'add_appointment.html'

    def get_success_url(self):
        return reverse('doctorlist', kwargs={'username': self.request.user.username})

    def get_initial(self):
        return {'user': self.request.user}
    
class AddDoctorView(CreateView):
    model = Doctor
    form_class = AddDoctorForm
    template_name = 'add_doctor.html'

    def get_success_url(self):
        return reverse('doctorlist', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        clinic, _ = get_clinic_and_objects(self.request.user)
        form.instance.clinic = clinic
        return super().form_valid(form)

    def get_initial(self):
        clinic, _ = get_clinic_and_objects(self.request.user)
        return {'clinic': clinic}   


class ChangePasswordView(FormView):
    template_name = 'change_password.html'
    form_class = ChangePasswordForm  # 改为自定义的表单类

    def get_object(self):
        customer_id = self.kwargs.get('customer_id')
        return get_object_or_404(Customer, pk=customer_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_object().user
        # 设置 old_password 的初始值
        kwargs['initial'] = {'old_password': 'password'}
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('customerlist', kwargs={'username': self.request.user.username})
    
    

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','fullname', 'age', 'sex', 'phonenumber','login_status']
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'is_staff', 'customer']





class RegisterUserAPIView(APIView):
    permission_classes = []

    def post(self, request):
        # 解析请求数据
        username = request.data.get('username')
        password = request.data.get('password')
        customer_data = request.data.get('customer')

        # 验证用户名是否重复
        if User.objects.filter(username=username).exists():
            return Response({'error': 'This username is already taken.'}, status=400)

        # 创建 User 对象
        user = User.objects.create_user(username=username, password=password)

        # 创建 Customer 对象，并关联到 User 对象上
        customer = Customer.objects.create(
            user=user,
            fullname=customer_data.get('fullname'),
            age=customer_data.get('age'),
            sex=customer_data.get('sex'),
            phonenumber=customer_data.get('phonenumber'),
        )

        serializer = UserSerializer(user, context={'request': request})

        # 返回创建成功的 User 和 Customer 对象
        return Response(serializer.data)
    
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


from rest_framework.generics import ListAPIView
class AppointmentByCustomerAPIView(ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Appointment.objects.filter(customer_id=customer_id)
    
class AppointmentCreateView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        
        if serializer.is_valid():
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']
            fullname = serializer.validated_data['fullname']
            existing_appointment = Appointment.objects.filter(date=date, time=time, fullname=fullname).first()
            if existing_appointment:
                raise DuplicateAppointmentException()
            
            appointment = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.exceptions import APIException
    
class DuplicateAppointmentException(APIException):
    status_code = 400
    default_detail = 'Appointment with the same date, time, and fullname already exists.'    
    
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    basename = 'appointments'
    




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(customer__isnull=False).distinct()
    serializer_class = UserSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        return User.objects.filter(customer__isnull=False).distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    @action(detail=False, methods=['get'])
    def get_current_user(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = UserSerializer(user, context={'request': request})
            print(serializer.data)
            return Response(serializer.data)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        print(f"Received login username: {username}")
        print(f"Received login password: {password}")

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            user.customer.login_status = True
            user.customer.save()
            return Response({'success': True, 'user_id': user.id})
        else:
            return Response({'success': False, 'message': 'Invalid username or password'})

        

class LogoutAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None or not user.is_authenticated:
            return Response({'success': False, 'message': 'User is not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        customer = user.customer
        if not customer.login_status:
            return Response({'success': False, 'message': 'User is already logged out'})

        logout(request)

        # 更新 login_status
        customer.login_status = False
        customer.save()

        print(f"User {username} has logged out.")
        return Response({'success': True, 'message': f'Logout success for user {username}'})



    
class DoctorSerializer(serializers.ModelSerializer):
    clinic = serializers.PrimaryKeyRelatedField(queryset=Clinic.objects.all())

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'state', 'clinic']


class ClinicSerializer(serializers.ModelSerializer):
    doctors = serializers.SerializerMethodField()

    class Meta:
        model = Clinic
        fields = ('id', 'clinicname', 'location', 'telnum', 'state', 'doctors')

    def get_doctors(self, obj):
        doctors = obj.doctors.filter(state='onduty')
        doctor_serializer = DoctorSerializer(doctors, many=True)
        return doctor_serializer.data


class ClinicListAPIView(APIView):
    def get(self, request, format=None):
        clinics = Clinic.objects.filter(state='open')
        serializer = ClinicSerializer(clinics, many=True)
        return Response(serializer.data)


class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    basename = 'clinics'

class DoctorListAPIView(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    basename = 'doctors'






class ChatLogAPIView(APIView):

    def post(self, request, format=None):
        sender = request.data.get('sender')
        message = request.data.get('message')
        user_id = request.data.get('user_id')

        user = None
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass

        chat_log = ChatLog(sender=sender, message=message, user=user)
        chat_log.save()

        # 打印接收到的信息
        print(f"Sender: {sender}")
        print(f"Message: {message}")
        print(f"User ID: {user_id}")

        return Response({'status': 'success'})

class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = ['id','user','sender','message', 'timestamp', 'created_at']
  
       
class ChatLogViewSet(viewsets.ModelViewSet):
    queryset = ChatLog.objects.all()
    serializer_class = ChatLogSerializer
    basename = 'chatlogs'



class CurrentUserIDAPIView(APIView):
    permission_classes = []

    def get(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            return Response({'id': user_id})
        else:
            return Response({'error': 'User not authenticated'})

from django.middleware.csrf import get_token


class GetCSRFToken(View):
    def get(self, request):
        csrf_token = get_token(request)
        response = JsonResponse({'csrf_token': csrf_token})
        response.set_cookie('csrftoken', csrf_token)
        return response











    



