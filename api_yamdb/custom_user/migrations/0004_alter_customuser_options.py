# Generated by Django 3.2 on 2024-08-18 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0003_auto_20240818_1912'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ('username',), 'verbose_name': ('Пользователь',), 'verbose_name_plural': ('Пользователи',)},
        ),
    ]
