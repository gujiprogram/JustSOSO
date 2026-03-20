from django import forms
from .models import Poster


class MovieForm(forms.ModelForm):
    class Meta:
        model = Poster
        fields = ['search_keyword', 'poster']
