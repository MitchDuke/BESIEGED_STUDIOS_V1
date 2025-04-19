from django.urls import path
from .views import dashboard, order_detail

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
]
