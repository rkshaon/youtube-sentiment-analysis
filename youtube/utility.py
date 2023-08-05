import urllib.parse



def get_video_id(video_url):
    parsed_query = urllib.parse.urlparse(video_url)
    query_params = urllib.parse.parse_qs(parsed_query.query)

    return query_params.get('v', [None])[0]