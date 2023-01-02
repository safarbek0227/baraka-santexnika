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
    query.widget.attrs.update({'placeholder': 'qidiruv', 'onkeyup':'sumbit()'})
    time = forms.ChoiceField(choices = TIME)
    class Meta:
        model = HistoryProduct
        fields = ['mode','product']

    # def __init__(self, *args, **kwargs):
    #     super(Searchform, self).__init__(*args, **kwargs)
    #     self.fields['mode'].required = False

class ProductSearchform(forms.ModelForm):
    query = forms.CharField()
    query.widget.attrs.update({'placeholder': 'qidiruv', 'onkeyup':'sumbit()'})
    time = forms.ChoiceField(choices = TIME)
    class Meta:
        model = Product
        fields = ['group']