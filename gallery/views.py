from django.shortcuts import render


def gallery(request):
    return render(request, 'gallery/gallery.html')


def gallery_detail(request, id):
    return render(request, 'gallery/gallery_detail.html', {'id': id})
