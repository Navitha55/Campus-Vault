from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import EmployeeDetails, StudentDetail  # Fixed space spacing typo
from .serializer import EmployeeDetailSerializer, StudentDetailSerializer
from . import password

def home_page(req):
    if req.COOKIES.get('is_logged_in') == 'True':
        return redirect('dashboard')
    return render(req, 'index.html') 

def register(req):
    if req.method == 'POST':
        username_input = req.POST.get('name')
        email_input = req.POST.get('email')
        phone_input = req.POST.get('phn')
        password_input = req.POST.get('pass')
        confirm_pass = req.POST.get('conf-pass')

        if confirm_pass != password_input:
            messages.info(req, "Password Mismatch")
            return redirect('register')
        
        if EmployeeDetails.objects.filter(emp_name=username_input).exists():
            messages.error(req, "Username already exists. Please try another one.")
            return render(req, 'register.html')

        else:
            password_input = password.pass_hash(password_input)
        
        form_data = {
            'emp_name': username_input,
            'emp_email': email_input,
            'emp_phone': phone_input,
            'emp_pass': str(password_input) 
        }

        serializer = EmployeeDetailSerializer(data=form_data)
        if serializer.is_valid():
            serializer.save() 
            messages.success(req, "Registration successful!")
            return render(req, 'register.html', {'registration_success': True})
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(req, f"{field.capitalize()}: {error}")
            return render(req, 'register.html')

    return render(req, 'register.html')

def login(req):
    if req.method == 'POST':
        name = req.POST.get('user')
        pw = req.POST.get('pass')

        if not name or not pw:
            messages.info(req, "Invalid credentials")
            return redirect('login')
        
        try:
            emp_obj = EmployeeDetails.objects.get(emp_name=name)

            if password.check_pw(pw, emp_obj.emp_pass):
                messages.success(req, "Login successful!")
                response = render(req, 'login.html', {'login_success': True})
                response.set_cookie(key='user', value=name)
                response.set_cookie(key='is_logged_in', value='True', max_age=60*60)
                return response
            else:
                messages.error(req, "Invalid Password!")
                
        except EmployeeDetails.DoesNotExist:
            messages.error(req, "User not found!")

    return render(req, 'login.html') 

def dashboard(req):
    if req.COOKIES.get('is_logged_in') != 'True':
        messages.error(req, "Please login to access the dashboard.")
        return redirect('login')
        
    logged_in_user = req.COOKIES.get('user', 'Guest')
    students = StudentDetail.objects.all()  # Pull records directly here
    
    context = {
        'students': students,
        'user': logged_in_user
    }
    return render(req, 'dashboard.html', context)

def add_student(req):
    if req.COOKIES.get('is_logged_in') != 'True':
        messages.error(req, "Please login to add students.")
        return redirect('login')

    if req.method == 'POST':
        stu_name = req.POST.get('name')
        stu_roll = req.POST.get('roll')
        stu_branch = req.POST.get('branch')
        stu_section = req.POST.get('section')
        stu_place = req.POST.get('place')
        
        form_data = {
            'name': stu_name,
            'roll_no': stu_roll,
            'branch': stu_branch,
            'section': stu_section,
            'place': stu_place
        }

        serializer = StudentDetailSerializer(data=form_data)
        if serializer.is_valid():
            serializer.save() 
            messages.success(req, "Student added successfully!")
            return render(req, 'addStudent.html', {'registration_success': True})
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(req, f"{field.capitalize()}: {error}")
            return render(req, 'addStudent.html')

    return render(req, 'addStudent.html')

def delete_student_view(req, pk):
    if req.COOKIES.get('is_logged_in') == 'True':
        student = get_object_or_404(StudentDetail, pk=pk)
        student.delete()
    return redirect('dashboard')

def edit_student_view(req, pk):
    if req.COOKIES.get('is_logged_in') != 'True':
        messages.error(req, "Please login to edit student profiles.")
        return redirect('login')
    
    student = get_object_or_404(StudentDetail, pk=pk)

    if req.method == 'POST':
        form_data = {
            'name': req.POST.get('name'),
            'roll_no': req.POST.get('roll'),
            'branch': req.POST.get('branch'),
            'section': req.POST.get('section'),
            'place': req.POST.get('place')
        }

        serializer = StudentDetailSerializer(instance=student, data=form_data)
        if serializer.is_valid():
            serializer.save()
            messages.success(req, "Student details updated successfully!")
            return redirect('dashboard')
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(req, f"{field.capitalize()}: {error}")

    return render(req, 'editStudent.html', {'student': student})


def logout(request):
    response = redirect('home_page')  
    response.delete_cookie('user')
    response.delete_cookie('is_logged_in')
    return response
