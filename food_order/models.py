from django.db import models


class Employee(models.Model):
    """ Модель сотрудника """

    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)
    department = models.CharField(max_length=25)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Dish(models.Model):
    """ Модель блюда """

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50,
                            unique=True)
    image = models.ImageField(upload_to='dish/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    composition = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name


class Order(models.Model):
    """ Модель заказа """

    employee = models.ForeignKey(Employee,
                                 related_name='orders',
                                 on_delete=models.CASCADE)
    date = models.DateTimeField(auto_created=True)
