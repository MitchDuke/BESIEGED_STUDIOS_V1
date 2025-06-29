from django.urls import path
from .views import dashboard, order_detail, edit_profile

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]
