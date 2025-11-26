from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import EmailVerification
from .forms import SignUpForm, VerificationForm
from django.contrib.auth import login as auth_login
import random


# Create your views here.

def home(request):
    return HttpResponse("start new project")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # deactivate until verified
            user.save()
            
            # Generate 4-digit code
            code = str(random.randint(1000, 9999))
            EmailVerification.objects.create(user=user, code=code)
            
            # Send code via email
            send_mail(
                'Your Verification Code',
                f'Your verification code is: {code}',
                'no-reply@example.com',
                [user.email],
                fail_silently=False
            )
            return redirect('verify', user_id=user.id)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def verify(request, user_id):
    user = User.objects.get(id=user_id)
    verification = EmailVerification.objects.get(user=user)
    
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == verification.code:
                # Mark verification as complete
                verification.is_verified = True
                verification.save()
                
                # Activate user
                user.is_active = True
                user.save()
                
                # Automatically log in the user
                auth_login(request, user)
                
                # Redirect to home after login
                return redirect('home')
            else:
                form.add_error('code', 'Invalid code')
    else:
        form = VerificationForm()
    
    return render(request, 'verify.html', {'form': form, 'email': user.email})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email, username=username)
        except User.DoesNotExist:
            user = None
        
        if user and user.check_password(password):
            if EmailVerification.objects.get(user=user).is_verified:
                auth_login(request, user)
                return redirect('home')  # redirect after login
            else:
                return render(request, 'login.html', {'error': 'Email not verified.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    return render(request, 'login.html')
