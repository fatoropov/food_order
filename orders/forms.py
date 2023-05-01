from django import forms
from .models import Order
from tempus_dominus.widgets import DateTimePicker


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        model.date = forms.DateTimeField(
                     widget=DateTimePicker(
                            options={
                                     'useCurrent': True,
                                     'collapse': False,
                                    },
                            attrs={
                                   'append': 'fa fa-calendar',
                                   'icon_toggle': True,
                                   }
                     ),
        )
        fields = ['name', 'date']
