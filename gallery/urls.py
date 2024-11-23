from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('<int:id>/', views.gallery_detail, name='gallery_detail'),
]
