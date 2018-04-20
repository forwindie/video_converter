from django import forms
from app.models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ('link', 'email')