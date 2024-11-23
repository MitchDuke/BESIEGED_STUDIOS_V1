from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('<int:id>/', views.dashboard_detail, name='dashboard_detail'),
]
