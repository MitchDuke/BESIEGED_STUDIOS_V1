from django.db import models
from django.contrib.auth.models import User


class CommissionQuote(models.Model):
    CATEGORY_CHOICES = [
        ('single_mini', 'Single Miniature'),
        ('squad', 'Squad'),
        ('colossal', 'Colossal Vehicle/Monster'),
        ('terrain', 'Terrain'),
    ]

    STATUS_CHOICES = [
        ('ready', 'Ready to Checkout'),
        ('pending', 'Pending Manual Quote'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    size_option = models.CharField(max_length=50, blank=True)
    assembly_required = models.BooleanField(default=False)
    priming_required = models.BooleanField(default=False)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    assembly_cost = models.DecimalField(max_digits=6, decimal_places=2)
    priming_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    size_uplift = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='commission_uploads/', blank=True, null=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ready')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission by {self.user} ({self.get_category_display()})"
