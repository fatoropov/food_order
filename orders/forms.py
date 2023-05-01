from django import forms
from .models import Order
# from tempus_dominus.widgets import DateTimePicker
# from .widgets import BootstrapDateTimePickerInput


class OrderCreateForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(
                                format='%d-%m-%Y-%HH-%mm',
                                attrs={'type': 'date'}),
                           required=False)

    class Meta:
        model = Order
        fields = ['name', 'date']
