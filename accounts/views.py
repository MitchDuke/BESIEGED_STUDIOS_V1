from django.shortcuts import render


def accounts(request):
    return render(request, 'accounts/accounts.html')


def accounts_detail(request, id):
    return render(request, 'accounts/accounts_detail.html', {'id': id})
