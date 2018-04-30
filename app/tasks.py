from __future__ import absolute_import
import os
import logging
import youtube_dl
from celery import shared_task
from django.core.mail import send_mail
from app.models import Query
from app.models import Audio


logger = logging.getLogger(__name__)


def my_hook(d):
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        print("Done downloading {}".format(file_tuple[1]))
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'])


@shared_task
def extract_audio_link(user_id):
    query = Query.objects.get(pk=user_id)
    link = query.link
    email = query.email

    with youtube_dl.YoutubeDL() as ydl:
        audio_info = ydl.extract_info(link, download=False)
    if audio_info:
        formats = audio_info['formats'][0]
        audio_title = audio_info.get('title')
        audio_size = formats.get('filesize')
        audio_url = formats.get('url')
        audio = Audio.objects.create(
            title=audio_title,
            size=audio_size,
            download_url=audio_url)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

#        with youtube_dl.YoutubeDL(ydl_opts) as ydl:  Здесь по идее надо загружать сконвертированный файл и сохранять
        audio.save()

        send_email_for_new_query.delay(email, audio_title, audio_url)


@shared_task
def send_email_for_new_query(email, audio_title, audio_url):
    send_mail(
        'Забирай свой мпЗ %s' % audio_title,
        'Вот тебе ссылка: %s' % audio_url,
        'emailsforsabina@gmail.com',
        [email],
        fail_silently=False,
    )
