from django import forms


class SearchForm(forms.Form):
    surnameSearch = forms.CharField()

