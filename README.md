# Руководство
## Установка
- Установить python3
- Создать виртуальное окружение `python -m venv .venv`
- Активировать виртуальное окружение `source .venv/bin/activate`
- Установить зависимости `pip install -r requirements.txt`
- Обновить переменные окружения `nano .env`
- Внести логин и пароль почтового сервиса:
	+ `export EMAIL_HOST_USER='***'`
	+ `export EMAIL_HOST_PASSWORD='***'`
- Активировать переменные окружения `source ./.env`
## Запуск
Запустить приложение командой:  
`python manage.py runserver`
