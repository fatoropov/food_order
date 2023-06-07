from django import forms
from django.contrib.auth.models import User
from .models import Employee


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя')
    first_name = forms.CharField(label='Имя')
    email = forms.EmailField(label='Почта')
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email неправильного формата')
        return data


class EmployeeRegistrationForm(forms.ModelForm):
    company = forms.CharField(label='Название компании')

    class Meta:
        model = Employee
        fields = ['company']

    def clean_company(self):
        cd = self.cleaned_data
        return cd['company']


class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя')
    first_name = forms.CharField(label='Имя')
    email = forms.EmailField(label='Почта')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
                         .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email неправильного формата')
        return data


class EmployeeEditForm(forms.ModelForm):
    company = forms.CharField(label='Название компании')

    class Meta:
        model = Employee
        fields = ['company']
