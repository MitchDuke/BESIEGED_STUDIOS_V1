from django.shortcuts import render


def commissions(request):
    return render(request, 'commissions/commissions.html')


def commissions_detail(request, id):
    return render(request, 'commissions/commissions_detail.html', {'id': id})
