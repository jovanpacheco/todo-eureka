from django import forms
from .models import List,Item


class ListForm(forms.ModelForm):

    # name = forms.CharField(
    #     label='',
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={'placeholder': 'Enter ToDo item'})
    # )
    # priority = forms.IntegerField(
    #     label='',
    #     required=True
    # )


    class Meta:
        model = List
        fields = ('name','priority','author')


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
    priority = forms.IntegerField(
        label='',
        required=True
    )

    class Meta:
        model = Item        
 