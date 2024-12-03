from django.shortcuts import render
from .models import Project


def gallery(request):
    projects = Project.objects.all()
    return render(request, 'gallery/gallery.html')


def gallery_detail(request, id):
    return render(request, 'gallery/gallery_detail.html', {'id': id})
