from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('<int:id>/', views.accounts_detail, name='accounts_detail'),
]
