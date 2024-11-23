from django.shortcuts import render


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def dashboard_detail(request, id):
    return render(request, 'dashboard/dashboard_detail.html', {'id': id})
