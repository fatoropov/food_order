from django import forms
from .models import Order
from food_order.models import Employee


class OrderCreateForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Employee.objects.all())
    date = forms.DateField(widget=forms.DateInput(
                                format='%d-%m-%Y-%HH-%mm',
                                attrs={'type': 'date'}),
                           required=False,
                           label="Выберите дату")

    class Meta:
        model = Order
        fields = ['name', 'date']
