from django import forms
from .models import CommissionRequest


class CommissionForm(forms.ModelForm):
    """Form for creating/editing commission requests."""
    class Meta:
        model = CommissionRequest
        fields = [
            'title', 'commission_type', 'size',
            'description', 'reference_images',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Chibi Portrait of My Cat',
            }),
            'commission_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_commission_type',
            }),
            'size': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 1080x1080px, A3, large poster',
                'id': 'id_size',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe what you want in detail...',
                'id': 'id_description',
            }),
            'reference_images': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
