from django.urls import path
from . import views

app_name = 'commissions'

urlpatterns = [
    path('create/', views.create_commission_quote, name='create_commission'),
    path('', views.commissions, name='commissions'),
    path('<int:id>/', views.commissions_detail, name='commissions_detail'),
]
