from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from .models import Mailing, MailingLog


def send_mailing(mailing: Mailing) -> dict:
    """
    Отправляет рассылку всем получателям.
    Возвращает словарь: {'success': N, 'failed': M, 'error': '...' или None}
    """
    now = timezone.now()

    if not (mailing.start_time <= now <= mailing.end_time): # проверка что время подходящее
        return {
            'success': 0,
            'failed': 0,
            'error': 'Текущее время вне периода рассылки'
        }

    recipients = mailing.recipients.all() # Проверяем получателей
    if not recipients.exists():
        return {
            'success': 0,
            'failed': 0,
            'error': 'У рассылки нет получателей'
        }

    success_count = 0
    failed_count = 0

    for recipient in recipients: # Отправляем
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            MailingLog.objects.create(
                mailing=mailing,
                status=MailingLog.STATUS_SUCCESS,
                server_response='OK'
            )
            success_count += 1
        except Exception as e:
            MailingLog.objects.create(
                mailing=mailing,
                status=MailingLog.STATUS_FAILURE,
                server_response=str(e)
            )
            failed_count += 1

    return {
        'success': success_count,
        'failed': failed_count,
        'error': None
    }