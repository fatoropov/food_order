from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, UserRegistrationForm, \
                   EmployeeEditForm, EmployeeRegistrationForm
from .models import Employee


def register(request):
    if request.method == 'POST':
        employee_form = EmployeeRegistrationForm(request.POST)
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():

            new_user = user_form.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data['password'])

            new_user.save()
            employee_company = employee_form.save(commit=False)
            employee_company = employee_form.cleaned_data['company']

            Employee.objects.create(user=new_user, company=employee_company)
            login(request, new_user)
            return render(request,
                          'food_order/index.html')
    else:
        user_form = UserRegistrationForm()
        employee_form = EmployeeRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form,
                   'employee_form': employee_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        employee_form = EmployeeEditForm(instance=request.user.employee,
                                         data=request.POST,
                                         files=request.FILES)
        if user_form.is_valid() and employee_form.is_valid():
            user_form.save()
            employee_form.save()
            messages.success(request, 'Профиль успешно обновлен')
        else:
            messages.error(request, 'Ошибка обновления профиля')
    else:
        user_form = UserEditForm(instance=request.user)
        employee_form = EmployeeEditForm(instance=request.user.employee)
    return render(request,
                  'registration/edit.html',
                  {'user_form': user_form,
                   'employee_form': employee_form})
