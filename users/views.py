from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import UserData

import random
import csv


# REGISTER

def register_page(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Username Check
        if User.objects.filter(username=username).exists():

            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        # Email Check
        if User.objects.filter(email=email).exists():

            return render(request, 'register.html', {
                'error': 'Email already registered'
            })

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Store Session
        request.session['otp'] = str(otp)
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password

        # Send OTP Email
        try:

            send_mail(
                'OTP Verification',
                f'Your OTP is: {otp}',
                'rakshitad76@gmail.com',
                [email],
                fail_silently=True,
            )

        except:
            pass

        return redirect('/verify-otp/')

    return render(request, 'register.html')


# VERIFY OTP

def verify_otp(request):

    if request.method == 'POST':

        entered_otp = request.POST['otp']

        saved_otp = request.session.get('otp')

        if entered_otp == saved_otp:

            username = request.session.get('username')
            email = request.session.get('email')
            password = request.session.get('password')

            # Final Checks
            if User.objects.filter(username=username).exists():

                return render(request, 'verify_otp.html', {
                    'error': 'Username already exists'
                })

            if User.objects.filter(email=email).exists():

                return render(request, 'verify_otp.html', {
                    'error': 'Email already exists'
                })

            # Create User
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Clear Session
            request.session.flush()

            return redirect('/')

        else:

            return render(request, 'verify_otp.html', {
                'error': 'Invalid OTP'
            })

    return render(request, 'verify_otp.html')


# LOGIN

def login_page(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/dashboard/')

        else:

            return render(request, 'login.html', {
                'error': 'Invalid Username or Password'
            })

    return render(request, 'login.html')


# DASHBOARD

@login_required
def dashboard(request):

    if request.method == 'POST':

        name = request.POST['name']

        UserData.objects.create(
            user=request.user,
            entered_name=name
        )

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = f'attachment; filename="{name}.csv"'

        writer = csv.writer(response)

        writer.writerow([
            'Name',
            'Email'
        ])

        writer.writerow([
            name,
            request.user.email
        ])

        return response

    data = UserData.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {
        'data': data
    })


# LOGOUT

def logout_page(request):

    logout(request)

    return redirect('/')