from django.shortcuts import render
from django.http import HttpResponseRedirect
from app.forms import QueryForm


def index(request):
    if request.method == "POST":
        form = QueryForm(request.POST or None)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('vsyo-budet.html')
    else:
        form = QueryForm()
    return render(request, 'index.html', {'form': form})


def ok(request):
    return render(request, 'vsyo-budet.html', {})

