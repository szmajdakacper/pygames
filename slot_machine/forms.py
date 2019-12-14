from django import forms

class PlayForm(forms.Form):
    rate = forms.IntegerField(initial=100, widget=forms.TextInput(attrs={'id':'rate'}))
    balance = forms.IntegerField(disabled=True, required=False, widget=forms.TextInput(attrs={'id':'balance'}))