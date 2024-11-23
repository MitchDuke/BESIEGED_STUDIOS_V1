from django.shortcuts import render, redirect


def login_view(request):
    return render(request, 'accounts/login.html')


def logout_view(request):
    return redirect('home')  # Placeholder, logout logic to be added.


def register_view(request):
    return render(request, 'accounts/register.html')
