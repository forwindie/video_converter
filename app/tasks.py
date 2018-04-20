from __future__ import absolute_import
from celery import shared_task
import logging

from django.core.mail import send_mail
from app.models import Query


@shared_task
def send_email_for_new_query(query_id):

    try:
        query = Query.objects.get(pk=query_id)
        send_mail(
            'Забирай свой мпЗ',
            'Вот тебе ссылка: %s' % query.link,
            'emailsforsabina@gmail.com',
            [query.email],
            fail_silently=False,
        )

    except:
        logging.info('Не удалось отправить')
