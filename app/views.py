from django.shortcuts import render
from django.http import HttpResponseRedirect
from app.forms import QueryForm
import youtube_dl


def index(request):
    if request.method == "POST":
        form = QueryForm(request.POST or None)
        if form.is_valid:
            link = request.POST['link']

            options = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'outtmpl': u'%(id)s.%(ext)s',
                'noplaylist': True,
                'nocheckcertificate': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }

            with youtube_dl.YoutubeDL(options) as ydl:
                result = ydl.extract_info(link, download=False)
                print(result)

            form.save()
            return HttpResponseRedirect('vsyo-budet.html')
    else:
        form = QueryForm()
    return render(request, 'index.html', {'form': form})


def ok(request):
    return render(request, 'vsyo-budet.html', {})

