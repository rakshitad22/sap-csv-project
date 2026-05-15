from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import UserData
import csv


def register_page(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():

            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('/')

    return render(request, 'register.html')


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

    return render(request, 'login.html')


@login_required
def dashboard(request):

    if request.method == 'POST':

        name = request.POST['name']

        UserData.objects.create(
            user=request.user,
            entered_name=name
        )

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        writer = csv.writer(response)

        writer.writerow(['Name'])
        writer.writerow([name])

        return response

    data = UserData.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {'data': data})


def logout_page(request):
    logout(request)
    return redirect('/')