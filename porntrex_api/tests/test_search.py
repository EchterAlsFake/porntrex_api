from .. import Client
from base_api import BaseCore

core = BaseCore()
core.config.pages_concurrency = 1
core.config.videos_concurrency = 1

client = Client(core=core)
search = client.search(query="stepmom")

def test_search():
    for idx, video in enumerate(search):
        if idx == 5:
            break

        assert isinstance(video.title, str) and len(video.title) > 0