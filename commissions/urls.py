from django.urls import path
from . import views
from .views import CommissionQuoteDetailView

app_name = 'commissions'

urlpatterns = [
    path('create/', views.create_commission_quote, name='create_commission'),
    path('quote/<int:pk>/', CommissionQuoteDetailView.as_view(), name='commissions_detail'),
    path('quote/<int:pk>/delete/', views.delete_commission, name='delete_commission'),
    path('quote/<int:pk>/add-to-basket/', views.add_to_basket, name='add_to_basket'),
    path('go/', views.smart_commission_redirect, name='smart_commission_redirect'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
