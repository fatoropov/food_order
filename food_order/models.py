from django.db import models


class Employee(models.Model):
    """ Модель сотрудника """

    name = models.CharField(max_length=30)
    department = models.CharField(max_length=25)
