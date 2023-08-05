from django import forms


class LinkForm(forms.Form):
    link = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a YouTube Link'
        })
    )

