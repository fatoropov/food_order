from django.db import models
from django.conf import settings


class Employee(models.Model):
    """ Модель сотрудника """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                default=None)
    company = models.CharField(max_length=50,
                               default=None)

    def __str__(self):
        return self.company
