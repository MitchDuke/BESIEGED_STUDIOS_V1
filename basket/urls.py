from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('add/<int:pk>/', views.add_to_basket, name='add'),
]
