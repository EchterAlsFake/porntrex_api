from .. import Client, Video
from base_api.base import BaseCore

core = BaseCore()
core.config.videos_concurrency = 1
core.config.pages_concurrency = 1

client = Client()
model = client.get_model("https://www.porntrex.com/channels/nubile-films/")


def test_model_information():
    assert isinstance(model.name, str) and len(model.name) > 0
    assert isinstance(model.information, dict) and len(model.information) > 0


def test_model_videos():
    for idx, video in enumerate(model.videos()):
        if idx == 5:
            break

        assert isinstance(video, Video) and video.title is not None

