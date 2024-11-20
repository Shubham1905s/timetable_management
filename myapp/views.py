from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .models import Timetable, User
from .forms import TimetableForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()


def home(request):
    return render(request, 'home.html')

@login_required
def add_timetable(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            timetable_entry = form.save(commit=False)
            timetable_entry.user = request.user
            timetable_entry.save()
            messages.success(request, "Timetable entry added successfully.")
            return redirect('myapp:dashboard')  # Redirect to the dashboard
    else:
        form = TimetableForm()

    return render(request, 'add_timetable.html', {'form': form})

@login_required
def professor_dashboard(request):
    if request.user.is_professor:
        timetable = request.user.timetable_set.all()  # Query professor's timetable
        return render(request, 'professor_dashboard.html', {'timetable': timetable})
    return redirect('student_dashboard')

@login_required
def student_dashboard(request):
    if request.user.is_student:
        timetable = request.user.timetable_set.all()  # Query student's timetable
        return render(request, 'student_dashboard.html', {'timetable': timetable})
    return redirect('professor_dashboard')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_professor:
                return redirect('myapp:professor_dashboard')
            else:
                return redirect('myapp:student_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request, user)
    return redirect('myapp:login')
                
def send_slot_notification(professor_email, message):
    send_mail(
        'Timetable Slot Update',
        message,
        'your_email@example.com',
        [professor_email],
        fail_silently=False,
    )
    
@login_required
def dashboard_view(request):
    timetable = Timetable.objects.filter(user=request.user)
    if not timetable.exists():
        timetable = None  # Set to None if no timetable is found
    return render(request, 'dashboard.html', {'timetable': timetable})

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('myapp:register')

        # Check if email already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('myapp:register')

        # Create new user using custom model
        user = User.objects.create_user(username=email, password=password)
        user.save()

        # Log the user in after registration
        login(request, user)

        # Redirect to dashboard (or any other page after successful registration)
        if user.is_professor:
            return redirect('myapp:professor_dashboard')
        else:
            return redirect('myapp:student_dashboard')

    return render(request, 'register.html')
