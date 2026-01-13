from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

# 1. Login/Home Page
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'index.html', {'form': form})

# 2. Registration Logic
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 3. Logout Logic - FIXED REDIRECT NAME
def logout_view(request):
    logout(request)
    return redirect('login') 

# 4. Dashboard + Profile Update + Analytics
@login_required
def dashboard(request):
    # Initialize Session Data to avoid Errors
    if 'my_reports' not in request.session:
        request.session['my_reports'] = [
            {'upload_date': 'Oct 15, 2023', 'report_name': 'Routine Check', 'bp': 128, 'sugar': 105, 'chol': 205, 'hb': 13.1},
            {'upload_date': 'Oct 01, 2023', 'report_name': 'Initial Panel', 'bp': 135, 'sugar': 110, 'chol': 215, 'hb': 12.5},
        ]
    
    if 'user_profile' not in request.session:
        request.session['user_profile'] = {
            'full_name': request.user.username,
            'email': request.user.email if request.user.email else "user@health.com",
            'dob': '',
            'gender': 'Not Set',
            'phone': 'Not Set',
            'blood_group': 'Not Set'
        }

    show_analytics = False

    if request.method == 'POST':
        # Action A: File Upload
        if request.FILES.get('medical_file'):
            new_report = {
                'upload_date': datetime.date.today().strftime("%b %d, %Y"),
                'report_name': request.FILES['medical_file'].name,
                'bp': 115, 'sugar': 88, 'chol': 170, 'hb': 14.8
            }
            reports = request.session['my_reports']
            reports.insert(0, new_report)
            request.session['my_reports'] = reports
            request.session.modified = True
            show_analytics = True 

        # Action B: Profile Update
        elif 'update_profile' in request.POST:
            request.session['user_profile'] = {
                'full_name': request.POST.get('full_name'),
                'email': request.POST.get('email'),
                'dob': request.POST.get('dob'),
                'gender': request.POST.get('gender'),
                'phone': request.POST.get('phone'),
                'blood_group': request.POST.get('blood_group'),
            }
            request.session.modified = True

    # Safely get profile data for the template
    profile = request.session.get('user_profile', {})
    latest = request.session['my_reports'][0] if request.session['my_reports'] else {}

    context = {
        'username': profile.get('full_name'),
        'user_email': profile.get('email'),
        'user_dob': profile.get('dob'),
        'user_gender': profile.get('gender'),
        'user_phone': profile.get('phone'),
        'user_blood_group': profile.get('blood_group'),
        'latest': latest,
        'reports': request.session['my_reports'],
        'show_analytics': show_analytics
    }
    return render(request, 'dashboard.html', context)

def password_reset_request(request):
    if request.method == 'POST':
        username_input = request.POST.get('email') 
        pin_input = request.POST.get('pin')
        new_pass = request.POST.get('new_password')

        if pin_input == "1234":
            try:
                # This is why we need 'from django.contrib.auth.models import User'
                user = User.objects.get(username=username_input)
                user.set_password(new_pass)
                user.save()
                messages.success(request, "Success! Password has been updated.")
                return redirect('login') 
            except User.DoesNotExist:
                messages.error(request, "Error: That username does not exist.")
        else:
            messages.error(request, "Error: Invalid Security PIN.")
            
    return render(request, 'password_reset.html')