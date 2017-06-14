from django import forms
from .models import List,Item


class ListForm(forms.Form):

    name = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter ToDo item'})
    )
    priority = forms.IntegerField(
        label='',
        required=True
    )


    class Meta:
        model = List


class ItemForm(forms.Form):

    title = forms.CharField(
        label='',
        required=True
    )
    list = forms.Select()
    assigned_to = forms.IntegerField(
        label='',
        required=True
    )
    note = forms.CharField(
        required=True
    )


    class Meta:
        model = Item        
 