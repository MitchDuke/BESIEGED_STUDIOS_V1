from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('<int:id>/', views.gallery_detail, name='gallery_detail'),
]
