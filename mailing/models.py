from django.db import models


class Recipient(models.Model):
    email = models.EmailField(max_length=150, unique=True, verbose_name='email', help_text='Введите email')
    full_name = models.CharField(max_length=150, verbose_name='Ф.И.О.', help_text='Введите Ф.И.О.')
    comment = models.TextField(max_length=2000, blank=True, verbose_name='Комментарий', help_text='Ваш комментарий...')

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'

    def __str__(self):
        return f"{self.full_name} ({self.email})"

