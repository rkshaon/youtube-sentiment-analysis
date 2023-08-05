from django.template import loader
from django.http import HttpResponse

from pytube import YouTube

from youtube.forms import LinkForm



def index(request):
    form = LinkForm()

    data = {}

    if request.method == 'POST':
        video = YouTube(url=request.POST['link'])
        data['title'] = video.title
        data['length'] = video.length
        data['author'] = video.author
        data['length'] = f"{ data['length'] // 60 }:{ data['length'] % 60}"

    context = {
        'form': form,
        'data': data,
    }
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))