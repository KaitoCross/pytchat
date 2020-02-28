import json 
import re
import requests
from .. import config
from .. import util
from ..exceptions import InvalidVideoIdException 

headers = config.headers

pattern = re.compile(r"yt\.setConfig\({'PLAYER_CONFIG': ({.*})}\);")

item_channel_id =[
    "videoDetails",
    "embeddedPlayerOverlayVideoDetailsRenderer",
    "channelThumbnailEndpoint",
    "channelThumbnailEndpoint",
    "urlEndpoint",
    "urlEndpoint",
    "url"
]

item_renderer = [
    "embedPreview",
    "thumbnailPreviewRenderer"
]

item_response = [
    "args",
    "embedded_player_response"
]

item_author_image =[
    "videoDetails",
    "embeddedPlayerOverlayVideoDetailsRenderer",
    "channelThumbnail",
    "thumbnails",
    0,
    "url"
]

item_thumbnail = [
    "defaultThumbnail",
    "thumbnails",
    2,
    "url"
]

item_channel_name = [
    "videoDetails",
    "embeddedPlayerOverlayVideoDetailsRenderer",
    "expandedRenderer",
    "embeddedPlayerOverlayVideoDetailsExpandedRenderer",
    "title",
    "runs",
    0,
    "text"
]

item_moving_thumbnail = [
    "movingThumbnail",
    "thumbnails",
    0,
    "url"
]

class VideoInfo:
    '''
    VideoInfo object retrieves YouTube video informations
    from the video page.

    Parameter
    ---------
    video_id : str

    Exception
    ---------
    InvalidVideoIdException :
        Occurs when video_id does not exist on YouTube.
    '''
    def __init__(self, video_id):
        self.video_id = video_id
        text = self._get_page_text(video_id)
        self._parse(text)

    def _get_page_text(self, video_id):
        url = f"https://www.youtube.com/embed/{video_id}"
        resp = requests.get(url, headers = headers)
        resp.raise_for_status()
        return resp.text

    def _parse(self, text):
        result = re.search(pattern, text)
        res= json.loads(result.group(1))
        response = self._get_item(res, item_response)
        if response is None:
            raise InvalidVideoIdException(
                f"Specified video_id [{self.video_id}] is invalid.")
        self._renderer = self._get_item(json.loads(response), item_renderer)
        if self._renderer is None:
            raise InvalidVideoIdException(
                f"No renderer found in video_id: [{self.video_id}].")

    def _get_item(self, dict_body, items: list):
        for item in items:
            if dict_body is None:
                break
            if isinstance(dict_body, dict):
                dict_body = dict_body.get(item)
                continue
            if isinstance(item, int) and \
               isinstance(dict_body, list) and \
               len(dict_body) > item:
                dict_body = dict_body[item]
                continue
            return None
        return dict_body

    def get_duration(self):
        duration_seconds = self._renderer.get("videoDurationSeconds")
        if duration_seconds:
            '''Fetched value is string, so cast to integer.'''
            return int(duration_seconds)
        '''When key is not found, explicitly returns None.'''
        return None

    def get_title(self):
        print(self._renderer)
        if self._renderer.get("title"):
            return [''.join(run["text"]) 
                for run in self._renderer["title"]["runs"]][0]
        return None

    def get_channel_id(self):
        channel_url = self._get_item(self._renderer, item_channel_id)
        if channel_url:
            return channel_url[9:]
        return None

    def get_author_image(self):
        return self._get_item(self._renderer, item_author_image) 

    def get_thumbnail(self):
        return self._get_item(self._renderer, item_thumbnail)

    def get_channel_name(self):
        return self._get_item(self._renderer, item_channel_name)
    
    def get_moving_thumbnail(self):
        return self._get_item(self._renderer, item_moving_thumbnail)
