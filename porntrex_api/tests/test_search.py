from .. import Client
from base_api import BaseCore
import pytest

@pytest.mark.asyncio
async def test_all():



    core = BaseCore()
    core.config.pages_concurrency = 1
    core.config.videos_concurrency = 1

    client = Client(core=core)
    search = client.search(query="stepmom")

    idx = 0
    async for video in search:
        await video.init()

        idx += 1
        assert isinstance(video.title, str)
        if idx == 5:
            break
