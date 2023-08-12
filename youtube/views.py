from django.template import loader
from django.http import HttpResponse

from pytube import YouTube
from googleapiclient.discovery import build
from langdetect import detect
from text2emotion import get_emotion

from youtube.forms import LinkForm

from youtube.utility import get_video_id
from youtube.utility import remove_emojis



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

            # # Again repeat
            # if 'nextPageToken' in video_response:
            #     video_response = youtube.commentThreads().list(
            #         part = 'snippet,replies',
            #         videoId = video_id,
            #           pageToken = video_response['nextPageToken']
            #     ).execute()
                
        data['comments'] = comments
        data['comments_count'] = len(comments)
        
        comments.append("I'm so excited to see you!")

        for comment in comments:
            try:
                language = detect(comment)

                if language == 'en':
                    print(f"Get the emotion of text `{comment}`")
                    emotions = get_emotion(comment)
                    print(f"Emotion: {emotions}\n")

            except Exception as e:
                print(f"Error: {e}")

    context = {
        'form': form,
        'data': data,
    }
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))