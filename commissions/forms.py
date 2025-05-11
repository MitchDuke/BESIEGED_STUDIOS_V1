from django import forms
from .models import CommissionQuote


class CommissionQuoteForm(forms.ModelForm):
    class Meta:
        model = CommissionQuote
        fields = [
            'quote_type',
            'subtype',
            'size',
            'assembly_required',
            'priming_required',
            'description',
            'reference_image',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }