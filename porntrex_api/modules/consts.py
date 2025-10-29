import re

from typing import List
from bs4 import BeautifulSoup

PATTERN_URL_KEY = re.compile(r"^video_(?:alt_)?url(?:\d+)?$", re.I)       # video_url, video_alt_url, video_alt_url2, ...
PATTERN_RESOLUTION_TEXT = re.compile(r"(\d{3,4})p", re.I)                 # "480p", "1080p FHD", "2160p 4K"
PATTERN_RESOLUTION_IN_URL = re.compile(r"_(\d{3,4})p\.mp4/?$", re.I)      # "..._720p.mp4" or "..._2160p.mp4"
PATTERN_MP4 = re.compile(r"\.mp4/?$", re.I)


def extractor_html(content: str) -> List[str]:
    soup = BeautifulSoup(content, "lxml")

    video_urls = []
    containers = soup.find_all("div", class_="video-preview-screen video-item thumb-item")
    for container in containers:
        video_urls.append(container.find("a")["href"])

    print(video_urls)
    return video_urls
