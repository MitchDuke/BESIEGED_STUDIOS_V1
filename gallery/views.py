from django.shortcuts import render, get_object_or_404
from .models import Project


def gallery(request):
    projects = Project.objects.all()
    return render(request, 'gallery/gallery.html', {'projects': projects})


def gallery_detail(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, 'gallery/gallery_detail.html', {'project': project})
