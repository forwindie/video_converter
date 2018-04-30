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


class Audio(models.Model):
    class Meta:
        db_table = "audio_table"

    title = models.CharField(verbose_name='Название', max_length=300)
    size = models.IntegerField()
    download_url = models.TextField()
    media = models.FileField(upload_to='uploads/', null=True)

    objects = models.Manager()


