# Generated by Django 4.2 on 2023-06-06 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food_order', '0005_employee_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employee',
        ),
    ]