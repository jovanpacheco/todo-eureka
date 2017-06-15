from django import forms
from .models import List,Item

class ListForm(forms.ModelForm):

    class Meta:
        model = List
        fields = ('name','priority','author')


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('title','list','note','priority','author','assigned_to')


class ItemListForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('title','note','priority','author','assigned_to')        