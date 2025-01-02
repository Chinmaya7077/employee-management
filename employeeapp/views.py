
from django.shortcuts import render, HttpResponse,redirect
from .models import Employee,Role,Department
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from datetime import datetime
from django.db.models import Q


# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('index')  # Redirect to home or dashboard
    else:
        form = UserCreationForm()
    return render(request, 'employeeapp/signup.html', {'form': form})



# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('index')  # Redirect to home or dashboard
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'employeeapp/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('login')
    
   
# Create your views here.
# @login_required
def index(request):
    return render(request, 'employeeapp/index.html')



@login_required
def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'employeeapp/view_all_emp.html', context)

@login_required
def add_emp(request):
    if request.method == 'POST':
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp = Employee(first_name= first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept_id = dept, role_id = role, hire_date = datetime.now())
        new_emp.save()
        # return HttpResponse('Employee added Successfully')
        messages.success(request, "Employee added successfully!")
        return redirect('all_emp')  # Redirect to the employee list or another page

    elif request.method=='GET':
        dept_list = Department.objects.all()
        Role_list=Role.objects.all()
        return render(request, 'employeeapp/add_employee.html',{'dept_id': dept_list,'role_id':Role_list})
    else:
        return HttpResponse("An Exception Occured! Employee Has Not Been Added")

@login_required
def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except:
            return HttpResponse("Please Enter A Valid EMP ID")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'employeeapp/remove_emp.html',context)

@login_required
def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps': emps
        }
        return render(request, 'employeeapp/view_all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'employeeapp/filter_emp.html')
    else:
        return HttpResponse('An Exception Occurred')