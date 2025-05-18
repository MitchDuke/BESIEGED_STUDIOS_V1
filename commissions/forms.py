from django import forms
from .models import CommissionQuote


class CommissionQuoteForm(forms.ModelForm):
    class Meta:
        model = CommissionQuote
        fields = ['category', 'size_option', 'assembly_required', 'priming_required', 'notes', 'image']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'assembly_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'priming_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap classes
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['size_option'] = forms.ChoiceField(
            choices=[],
            required=True,
            widget=forms.Select(attrs={'class': 'form-select'})
        )
