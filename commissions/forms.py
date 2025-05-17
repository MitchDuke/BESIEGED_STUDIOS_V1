from django import forms
from .models import CommissionQuote


class CommissionQuoteForm(forms.ModelForm):
    class Meta:
        model = CommissionQuote
        fields = ['category', 'size_option', 'notes', 'image']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['size_option'] = forms.ChoiceField(
            choices=[],  # empty by default, populated dynamically
            required=True
        )
