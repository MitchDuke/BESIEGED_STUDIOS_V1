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

        # Dynamically populate size_option choices based on category
        if 'category' in self.data:
            category = self.data.get('category')
            self.fields['size_option'].choices = self.get_size_options(category)

    def get_size_options(self, category):
        """Return size options based on selected category"""
        CATEGORY_OPTIONS = {
            'single_mini': [
                ('small_hero', 'Small Hero (+0%)'),
                ('monster', 'Monster (+50%)'),
                ('tank', 'Tank/Walker (+75%)'),
            ],
            'squad': [
                ('1_5', 'Up to 5 Models (+10%)'),
                ('6_10', '6 to 10 Models (+10%)'),
                ('11_15', '11 to 15 Models (+10%)'),
                ('16_20', '16 to 20 Models (+15%)'),
                ('21_plus', '21+ Models (Case by Case)'),
            ],
            'colossal': [
                ('colossal_monster', 'Colossal Monster (+20%)'),
                ('colossal_vehicle', 'Colossal Vehicle (+20%)'),
                ('over_20cm', 'Over 20cm (Case by Case)'),
            ],
            'terrain': [
                ('10cm', '≤ 10cm Combined (+10%)'),
                ('20cm', '≤ 20cm Combined (+15%)'),
                ('40cm', '≤ 40cm Combined (+20%)'),
                ('50cm', '> 50cm Combined (Case by Case)'),
            ],
        }

        return CATEGORY_OPTIONS.get(category, [])
