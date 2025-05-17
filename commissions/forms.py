from django import forms
from .models import CommissionQuote


class CommissionQuoteForm(forms.ModelForm):
    class Meta:
        model = CommissionQuote
        fields = ['category', 'size_option', 'notes', 'image']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        size_option = cleaned_data.get('size_option')

        # Define base prices
        base_prices = {
            'single_mini': 50.00,
            'squad': 150.00,
            'colossal': 200.00,
            'terrain': 50.00,
        }

        # Uplift mapping
        uplifts = {
            'small': 0.10,
            'medium': 0.15,
            'large': 0.20,
        }

        # Define case-by-case keywords
        case_keywords = ['case by case', 'over 20', '21+', '50cm']

        # Case-by-case detection
        if any(keyword in size_option.lower() for keyword in case_keywords):
            cleaned_data['base_price'] = 0
            cleaned_data['assembly_cost'] = 0
            cleaned_data['total_price'] = 0
            cleaned_data['status'] = 'pending'
            return cleaned_data

        # Base price
        base_price = base_prices.get(category, 0)

        # Infer uplift %
        if any(term in size_option.lower() for term in ['0 to 5', 'small', '10cm']):
            uplift = uplifts['small']
        elif any(term in size_option.lower() for term in ['6 to 10', '20cm', 'medium']):
            uplift = uplifts['medium']
        else:
            uplift = uplifts['large']

        # Final calculated fields
        assembly_cost = base_price * uplift
        total_price = base_price + assembly_cost

        cleaned_data['base_price'] = base_price
        cleaned_data['assembly_cost'] = round(assembly_cost, 2)
        cleaned_data['total_price'] = round(total_price, 2)
        cleaned_data['status'] = 'ready'

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = self.cleaned_data

        instance.base_price = cleaned_data['base_price']
        instance.assembly_cost = cleaned_data['assembly_cost']
        instance.total_price = cleaned_data['total_price']
        instance.status = cleaned_data['status']

        if commit:
            instance.save()
        return instance
