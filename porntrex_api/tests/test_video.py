from ..porntrex_api import Client


client = Client()
video = client.get_video("https://www.porntrex.com/video/2989480/i-have-two-big-titties-and-im-your-date")

def test_attributes():
    assert isinstance(video.title, str) and len(video.title) > 0
    assert isinstance(video.json_data, dict) and len(video.video_metadata) > 0
    assert isinstance(video.description, str) and len(video.description) > 0
    assert isinstance(video.duration, str) and len(video.duration) > 0
    assert isinstance(video.video_id, str) and len(video.video_id) > 0
    assert isinstance(video.author, str) and len(video.author) > 0
    assert isinstance(video.categories, list) and len(video.categories) > 0
    assert isinstance(video.tags, list) and len(video.tags) > 0
    assert isinstance(video.subscribers_count, str) and len(video.subscribers_count) > 0
    assert isinstance(video.lrc, str) and len(video.lrc) > 0
    assert isinstance(video.license_code, str) and len(video.license_code) > 0
    assert isinstance(video.views, str) and len(video.views) > 0
    assert isinstance(video.rnd, str) and len(video.rnd) > 0
    assert isinstance(video.thumbnail, str) and len(video.thumbnail) > 0

def test_download():
    assert video.download(quality="worst") is True
