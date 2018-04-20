from django.contrib import admin
from django.db import models
from django.db.models import signals
from app.tasks import send_email_for_new_query


class Query(models.Model):
    class Meta:
        db_table = "query_table"

    email = models.EmailField(verbose_name='Email')
    link = models.URLField(verbose_name='Ссылка')
    query_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link

    objects = models.Manager()


def new_query(sender, instance, signal, *args, **kwargs):
    send_email_for_new_query.delay(instance.pk)


signals.post_save.connect(new_query, sender=Query)
