from django import forms
from .models import Order
from django.contrib.auth.models import User
from users.models import Employee

from datetime import date


class OrderCreateForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=User.objects.all(),
                                  label="Выберите имя",
                                  widget=forms.Select(
                                attrs={'class': 'form-control select mb-3'}))
    date = forms.DateField(widget=forms.DateInput(
                                format='%d-%m-%Y',
                                attrs={'type': 'date',
                                       'class': 'form-control mb-3'}),
                           required=True,
                           label="Выберите дату",
                           initial=date.today().strftime('%d-%m-%Y'))

    class Meta:
        model = Order
        fields = ['name', 'date']


class EmployeeCompanyForm(forms.ModelForm):
    company = forms.CharField(label='Название компании',
                              disabled=True)

    class Meta:
        model = Employee
        fields = ['company']

    def get_company(self):
        company_name = self.cleaned_data['company']
        return company_name
