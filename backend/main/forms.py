from django import forms
from .models import *

TIME = (
    ('','odatiy'),
    (3, '3 kun'),
    (7, 'bir hafta'),
    (30, 'bir oy'),
    )
class Searchform(forms.ModelForm):
    query = forms.CharField()
    query.widget.attrs.update({'placeholder': 'qidiruv'})
    time = forms.ChoiceField(choices = TIME)
    class Meta:
        model = HistoryProduct
        fields = ['mode','product']

    # def __init__(self, *args, **kwargs):
    #     super(Searchform, self).__init__(*args, **kwargs)
    #     self.fields['mode'].required = False

class CartFilter(forms.Form):
    query = forms.CharField()
    query.widget.attrs.update({'placeholder': 'qidiruv',})
    time = forms.ChoiceField(choices = TIME)


class ProductSearchform(forms.ModelForm):
    query = forms.CharField()
    query.widget.attrs.update({'placeholder': 'qidiruv', 'onkeyup':'sumbit()'})
    time = forms.ChoiceField(choices = TIME)
    class Meta:
        model = Product
        fields = ['group']

class CartForm(forms.ModelForm):
    class Meta:
        model = HistoryProduct
        fields = ['product', 'comment', 'quantity',]