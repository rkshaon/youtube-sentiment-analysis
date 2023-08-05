from django.template import loader
from django.http import HttpResponse

from youtube.forms import LinkForm



def index(request):
    form = LinkForm()

    if request.method == 'POST':
        print(f"\nLink: {request.POST['link']}\n")

    context = {
        'form': form,
    }
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))