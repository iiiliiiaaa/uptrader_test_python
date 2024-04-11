from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name='Родительский пункт меню', help_text='Не указывается для корневого пункта')
    url = models.CharField(max_length=200, blank=True, verbose_name='URL',
                           help_text='Должен быть указан, если не указан Именованный URL. Формат: /URL/')
    named_url = models.CharField(max_length=200, blank=True, verbose_name='Именованный URL',
                                 help_text='Нужно зарегистрировать path в urls.py')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ Получает URL пункта меню. """
        if self.named_url:
            try:
                return reverse(self.named_url)
            except:
                pass
        return self.url

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты Меню'
