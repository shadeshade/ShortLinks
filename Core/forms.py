from django import forms

from .models import Link


class LinkCreate(forms.ModelForm):
    class Meta:
        model = Link
        fields = (
            'main_part', 'subpart',
        )

        labels = {
            'main_part': 'Link',
            'subpart': 'Subpart'
        }

        widgets = {
            'main_part': forms.URLInput(attrs={'placeholder': 'Input page link', }),
            'subpart': forms.TextInput(attrs={'placeholder': 'Input your subpart if needed', }),
        }

    def __init__(self, *args, **kwargs):
        super(LinkCreate, self).__init__(*args, **kwargs)
        self.fields['subpart'].required = False
