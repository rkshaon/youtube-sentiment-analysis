from django.template import loader
from django.http import HttpResponse

from pytube import YouTube
from googleapiclient.discovery import build

from youtube.forms import LinkForm

from youtube.utility import get_video_id



def index(request):
    form = LinkForm()

    data = {}

    if request.method == 'POST':
        url = request.POST['link']
        comments = []
        continute_iterate = True

        video = YouTube(url=url)
        
        data['title'] = video.title
        data['length'] = video.length
        data['author'] = video.author
        data['length'] = f"{ data['length'] // 60 }:{ data['length'] % 60}"

        # API Key
        api_key = 'AIzaSyBTG3odetKiIyri53VTjU7DOFLAcRZYCs0'
        
        # Getting YouTube Video ID
        video_id = get_video_id(video_url=url)
        
        # creating youtube resource object
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # retrieve youtube video results
        video_response = youtube.commentThreads().list(part='snippet,replies',videoId=video_id).execute()

        while video_response and continute_iterate:
            for item in video_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                
                if comment not in comments:
                    comments.append(comment)
                else:
                    continute_iterate = False

            # Again repeat
            if 'nextPageToken' in video_response:
                video_response = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    videoId = video_id,
                      pageToken = video_response['nextPageToken']
                ).execute()
                
        data['comments'] = comments

    context = {
        'form': form,
        'data': data,
    }
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))