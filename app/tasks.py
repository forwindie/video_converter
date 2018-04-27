from __future__ import absolute_import
import os
import logging
import youtube_dl
from celery import shared_task
from django.core.mail import send_mail
from app.models import Query


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

    ydl_opts = {
        'extractaudio': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(link, download=False)
        video_title = result['title']
        video_url = result['url']    #здесь будет ссылка на сконвертированный файл

    send_email_for_new_query.delay(email, video_title, video_url)


@shared_task
def send_email_for_new_query(email, video_title, video_url):
    send_mail(
        'Забирай свой мпЗ %s' % video_title,
        'Вот тебе ссылка: %s' % video_url,
        'emailsforsabina@gmail.com',
        [email],
        fail_silently=False,
    )
