from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.urls import reverse_lazy
from . models import addemployee, addLeave, profile
from .forms import UserRegistrationForm, employeeLoginForm, AddLeaveForm, CustomUserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save

# Create your views here.

#home page
def index(request):
    #return render(request, 'index.html')
    return render(request, 'login.html')

#login for the superuser and normal employee
def login_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if user_type == 'superuser':
            user = authenticate(username=username, password=password)
            if user and user.is_superuser:
                login(request, user)
                return redirect('dashboard')
        elif user_type == 'normal_user':
            user = authenticate(username=username, password=password)
            if user and not user.is_superuser:
                login(request, user)                
                return redirect('dashboard')    
        return render(request, 'login.html')
    
#logout for the users
def logout(request):
    auth.logout(request)
    return redirect('demo')

#the main homepage after login is succesfull   
def dashboard(request):
    return render(request, 'home.html')

#template for applying leave for employees
def homeContent(request):
    return render(request, 'homecontent.html')


def leaveManagement(request):
    return render(request, 'leaveManagement.html')


#to add new users from the admin's side
class addemployee(CreateView):
    model = User
    form_class = UserCreationForm
    #fields = ['username', 'email', 'password1', 'password2']
    template_name = 'addEmployee.html'
    success_url = reverse_lazy('demo')

    def form_valid(self, form):
        self.object = form.save()
        #response = super().form_valid(form)
        user_id = self.object.id  # Access the ID of the created user (within form_valid)
        return super().form_valid(form)

#template to show the add leave button for the employees
def add_leaveContent(request):
    return render(request, 'addLeave.html')

#fun to add the leave for the employees
def add_leave(request):
    if request.method == 'POST':
        fromDate = request.POST['fromDate']
        toDate = request.POST['toDate']
        reason = request.POST['reason']
        comment = request.POST['comment']
        username = request.user.username
        user_id =  request.user.id
        status = 'pending'

        user_profile = profile.objects.get(user=request.user)
        if reason == 'casual leave':
            user_profile.remaining_casual_leaves -= 1
        elif reason == 'sick leave':
            user_profile.remaining_sick_leaves -= 1
        user_profile.save()

        leave = addLeave.objects.create(user_id=user_id, username=username, fromDate=fromDate,toDate=toDate, reason=reason, comment=comment, status=status)
        leave.save()
        return redirect('dashboard')
    else:
        return render(request, 'addLeave.html', {'leave': leave, 'user_profile': user_profile})

    
#fun to fetch all the leaves applied by the employees and to show only the title in template
def leave_content(request):
    list = addLeave.objects.all()
    return render(request, 'leaveApplications.html', {'lists': list})

#fun to fetch the leaves applied by the employees using the id and to display it in the template
def leave_lists(request, leave_id):
    leave_list = addLeave.objects.get(id=leave_id)
    return render(request, 'leaveApplicationdetails.html', {'leave_info': leave_list})


def pendingLeaves(request):
    return render(request, 'pendingLeaves.html')

@login_required
def leave_details(request):
    user_id = request.user.id
    leave_detailsss = addLeave.objects.filter(user_id=user_id)
    print(leave_detailsss)
    return render(request, 'pendingLeaves2.html', {'leave_details': leave_detailsss})

#@login_required
#def leave_applications(request):
    #if request.user.is_superuser:
        #leave_applications = LeaveApplication.objects.all()
    #else:
        #leave_applications = LeaveApplication.objects.filter(user=request.user)
    #return render(request, 'pendingLeaves3.html', {'leave_applications': leave_applications})

@login_required
def approve_leave(request, leave_id):
    if request.user.is_superuser:
        leave_application = addLeave.objects.get(pk=leave_id)
        leave_application.status = 'accepted'
        leave_application.save()
    return redirect('leave_content')

@login_required
def reject_leave(request, leave_id):
    if request.user.is_superuser:
        leave_application = addLeave.objects.get(pk=leave_id)
        leave_application.status = 'rejected'
        leave_application.save()
    return redirect('leave_content')