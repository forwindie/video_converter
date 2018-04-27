from django.contrib import admin
from django.db import models


class Query(models.Model):
    class Meta:
        db_table = "query_table"

    email = models.EmailField(verbose_name='Email')
    link = models.URLField(verbose_name='Ссылка')
    query_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link

    objects = models.Manager()


