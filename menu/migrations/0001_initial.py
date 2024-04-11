# Generated by Django 4.2.11 on 2024-04-11 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('url', models.CharField(blank=True, help_text='Должен быть указан, если не указан Именованный URL. Формат: /URL/', max_length=200, verbose_name='URL')),
                ('named_url', models.CharField(blank=True, help_text='Нужно зарегистрировать path в urls.py', max_length=200, verbose_name='Именованный URL')),
                ('parent', models.ForeignKey(blank=True, help_text='Не указывается для корневого пункта', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='menu.menuitem', verbose_name='Родительский пункт меню')),
            ],
            options={
                'verbose_name': 'Пункт меню',
                'verbose_name_plural': 'Пункты Меню',
            },
        ),
    ]