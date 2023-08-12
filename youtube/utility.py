import urllib.parse
import emoji



def get_video_id(video_url):
    parsed_query = urllib.parse.urlparse(video_url)
    query_params = urllib.parse.parse_qs(parsed_query.query)

    return query_params.get('v', [None])[0]


def remove_emojis(text):
    # clean_text = ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)
    return ''.join(c for c in text if c in emoji.UNICODE_EMOJI['en'])
    # return clean_text