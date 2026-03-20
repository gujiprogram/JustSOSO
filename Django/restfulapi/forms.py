from django import forms
from movies.models import Movie


class MovieInfo(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['search_keyword', 'name', 'link', 'description', 'size', 'access', 'alias', 'network', 'detail',
                  'rate']
