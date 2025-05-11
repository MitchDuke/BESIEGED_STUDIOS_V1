from django import forms
from .models import CommissionQuote


class CommissionQuoteForm(forms.ModelForm):
    class Meta:
        model = CommissionQuote
        fields = [
            'category',
            'size_option',
            'base_price',
            'assembly_cost',
            'total_price',
            'image',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
