from django.urls import path
from . import views

urlpatterns = [
    path('', views.commissions, name='commissions'),
    path('<int:id>/', views.commissions_detail, name='commissions_detail'),
]
