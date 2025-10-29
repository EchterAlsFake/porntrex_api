import re

PATTERN_URL_KEY = re.compile(r"^video_(?:alt_)?url(?:\d+)?$", re.I)       # video_url, video_alt_url, video_alt_url2, ...
PATTERN_RESOLUTION_TEXT = re.compile(r"(\d{3,4})p", re.I)                 # "480p", "1080p FHD", "2160p 4K"
PATTERN_RESOLUTION_IN_URL = re.compile(r"_(\d{3,4})p\.mp4/?$", re.I)      # "..._720p.mp4" or "..._2160p.mp4"
PATTERN_MP4 = re.compile(r"\.mp4/?$", re.I)