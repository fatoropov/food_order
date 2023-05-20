from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserEditForm


def register(request):
    if request.method != 'POST':
        # Выводит пустую форму регистрации.
        form = UserCreationForm()
    else:
        # Обработка заполненной формы.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Выполнение входа и перенаправление на домашнюю страницу.
            login(request, new_user)
            return redirect('food_order:dish_list')

    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Профиль успешно обновлен')
        else:
            messages.error(request, 'Ошибка обновления профиля')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request,
                  'registration/edit.html',
                  {'user_form': user_form})
