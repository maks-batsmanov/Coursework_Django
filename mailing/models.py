from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


class Recipient(models.Model):
    email = models.EmailField(max_length=150, unique=True, verbose_name='email', help_text='Введите email')
    full_name = models.CharField(max_length=150, verbose_name='Ф.И.О.', help_text='Введите Ф.И.О.')
    comment = models.TextField(max_length=2000, blank=True, verbose_name='Комментарий', help_text='Ваш комментарий...')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipients', verbose_name='Владелец', null=True, blank=True)


    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name='Тема сообщения')
    body = models.TextField(max_length=10000, verbose_name='Тело сообщения')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages', verbose_name='Владелец', null=True, blank=True)


    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f"{self.subject} {self.body}"


class Mailing(models.Model):
    STATUS_CREATED = 'Создана'
    STATUS_RUNNING = 'Запущена'
    STATUS_COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_RUNNING, 'Запущена'),
        (STATUS_COMPLETED, 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Старт рассылки')
    end_time = models.DateTimeField(verbose_name='Стоп рассылки')
    status = models.CharField(verbose_name='Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_CREATED)
    message = models.ForeignKey(Message, verbose_name='message', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, verbose_name='получатели')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mailings', verbose_name='Владелец', null=True, blank=True)
    is_disabled = models.BooleanField(default=False, verbose_name='Отключена')


    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def __str__(self):
        return f"Рассылка #{self.id} — Статус: {self.status}"

    def update_status(self):
        now = timezone.now()

        if now < self.start_time:
            new_status = self.STATUS_CREATED
        elif self.start_time <= now <= self.end_time:
            new_status = self.STATUS_RUNNING
        else:
            new_status = self.STATUS_COMPLETED

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])

    def send_mailing(self):
        now = timezone.now()

        if not self.start_time <= now <= self.end_time:
            raise ValueError('Неподходящее время для этой рассылки')

        recipients = self.recipients.all()

        if not recipients.exists():
            return 'У этой рассылки нет получателей'

        for recipient in recipients:
            try:
                send_mail(
                    subject=self.message.subject,
                    message=self.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient.email],
                    fail_silently=False
                )

                MailingLog.objects.create(mailing=self, status=MailingLog.STATUS_SUCCESS, server_response='Письмо успешно отправлено')

            except Exception as e:
                MailingLog.objects.create(
                    mailing=self,
                    status=MailingLog.STATUS_FAILURE,
                    server_response=str(e)
                )

    def clean(self):
        super().clean()
        now = timezone.now()

        if not self.pk and self.start_time < now:
            raise ValidationError({'start_time': 'Дата и время начала рассылки не могут быть в прошлом.'})

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError({'end_time': 'Дата окончания должна быть позже даты начала рассылки.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class MailingLog(models.Model):
    STATUS_SUCCESS = 'Успешно'
    STATUS_FAILURE = 'Не успешно'

    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAILURE, 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, verbose_name='Рассылка', on_delete=models.CASCADE, related_name='logs')
    datetime = models.DateTimeField(verbose_name='Дата и время попытки', auto_now_add=True)
    status = models.CharField(verbose_name='Статус попытки', choices=STATUS_CHOICES, max_length=20)
    server_response = models.TextField(verbose_name='Ответ сервера / Ошибка', blank=True, null=True)

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылок'

    def __str__(self):
        return f"Попытка для рассылки #{self.mailing.id} — {self.status}"


