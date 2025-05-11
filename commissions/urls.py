from django.urls import path
from . import views
from .views import CommissionQuoteDetailView

app_name = 'commissions'

urlpatterns = [
    path('create/', views.create_commission_quote, name='create_commission'),
    path('quote/<int:pk>/', CommissionQuoteDetailView.as_view(), name='commission_detail'),
    path('go/', views.smart_commission_redirect, name='smart_commission_redirect'),
]
