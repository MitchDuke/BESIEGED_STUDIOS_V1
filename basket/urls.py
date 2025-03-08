from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_view, name='basket_view'),
    path('adjust/<int:pk>/', views.adjust_basket, name='adjust'),
    path('remove/<int:pk>/', views.remove_from_basket, name='remove'),
]
