"""
Copyright (C) 2024-2025 Johannes Habel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import json5
import logging
import traceback

from functools import cached_property
from typing import Union, Generator, Optional, List, LiteralString, Tuple, Dict
from base_api.base import BaseCore, setup_logger, Helper, _choose_quality_from_list, _normalize_quality_value
from bs4 import BeautifulSoup

try:
    from modules.consts import *

except (ModuleNotFoundError, ImportError):
    from .modules.consts import *


class Video:
    def __init__(self, url: str, core: BaseCore):
        self.url = url
        self.core = core
        self.logger = setup_logger(name="PORNTREX API - [Video]", log_file=None, level=logging.ERROR)
        self.html_content = self.core.fetch(self.url)
        self.soup = BeautifulSoup(self.html_content, "lxml")
        self.video_metadata = self.soup.find("div", class_="video-info").find("div", class_="item")
        self.json_data = self.get_json_data()

    def enable_logging(self, log_file: str = None, level = None, log_ip: str = None, log_port: int = None):
        self.logger = setup_logger(name="PORNTREX API - [Video]", log_file=log_file, level=level, http_ip=log_ip, http_port=log_port)

    def get_json_data(self):
        # Grab the object literal after `var flashvars =`
        m = re.search(r"var\s+flashvars\s*=\s*({.*?})\s*;", self.html_content, re.S)
        obj_literal = m.group(1)
        return json5.loads(obj_literal)

    def _extract_height_for_key(self, key: str, url: str) -> Union[int, None]:
        """
        Try to get the numeric height from "<key>_text" first, then from the URL pattern.
        """
        # 1) From "<key>_text" if present (e.g., "720p HD")
        label = self.json_data.get(f"{key}_text")
        if label:
            m = PATTERN_RESOLUTION_TEXT.search(label)
            if m:
                return int(m.group(1))

        # 2) From the URL itself if it ends with "..._720p.mp4"
        m = PATTERN_RESOLUTION_IN_URL.search(url)
        if m:
            return int(m.group(1))

        # 3) Special-case fallback: the base "video_url" sometimes lacks "_480p" in the URL;
        #    use "video_url_text" if available.
        if key == "video_url":
            txt = self.json_data.get("video_url_text")
            if txt:
                m = PATTERN_RESOLUTION_TEXT.search(txt)
                if m:
                    return int(m.group(1))

        return None

    def _collect_height_url_pairs(self) -> List[Tuple[int, str]]:
        """
        Build (height, url) pairs from the JSON payload.
        Only keeps valid .mp4 URLs that have a resolvable height.
        Deduplicates by height (last one wins if duplicates found).
        """
        by_height: Dict[int, str] = {}
        for k, v in self.json_data.items():
            if not isinstance(v, str):
                continue
            if not PATTERN_URL_KEY.match(k):
                continue
            if not PATTERN_MP4.search(v):
                continue

            h = self._extract_height_for_key(k, v)
            if h is not None:
                by_height[h] = v

        # Sort by ascending height
        return sorted(by_height.items(), key=lambda kv: kv[0])

    def video_qualities(self) -> list:
        """
        :return: (list[str]) available qualities as e.g. ["480", "720", "1080", "2160"]
        """
        pairs = self._collect_height_url_pairs()
        heights = [str(h) for h, _ in pairs]
        return heights

    def direct_download_urls(self) -> list:
        """
        :return: (list[str]) direct MP4 URLs aligned in ascending order of quality.
                 Ordering matches the sorted `video_qualities`.
        """
        pairs = self._collect_height_url_pairs()
        urls = [url for _, url in pairs]
        return urls

    @cached_property
    def title(self) -> str:
        return self.json_data["video_title"]

    @cached_property
    def video_id(self) -> str:
        return self.json_data["video_id"]

    @cached_property
    def categories(self) -> List[str]:
        return self.json_data["video_categories"].split(",")

    @cached_property
    def tags(self) -> List[str]:
        return self.json_data["video_tags"].split(",")

    @cached_property
    def license_code(self) -> str:
        return self.json_data["license_code"]

    @cached_property
    def lrc(self) -> str:
        return self.json_data["lrc"]

    @cached_property
    def rnd(self) -> str:
        return self.json_data["rnd"]

    @cached_property
    def author(self) -> str:
        return self.soup.find("div", class_="username").find("a").text.strip()

    @cached_property
    def publish_date(self) -> str:
        return self.video_metadata.find("em").text.strip()

    @cached_property
    def views(self) -> str:
        return self.video_metadata.find_all("em")[1].text.strip()

    @cached_property
    def duration(self) -> str:
        return self.video_metadata.find_all("em")[2].text.strip()

    @cached_property
    def description(self) -> str:
        return self.soup.find("em", class_="des-link").text.strip()

    @cached_property
    def subscribers_count(self) -> str:
        return self.soup.find("div", class_="button-infow").text.strip()

    def download(self, quality, path: str = "./", callback=None, no_title: bool = False):
        """
        `quality` can be an int (e.g., 720) or "best" / "half" / "worst".
        """
        cdn_urls = self.direct_download_urls()
        quals = self.video_qualities()  # e.g., ["480", "720", "1080", "2160"]

        qn = _normalize_quality_value(quality)
        chosen_height = _choose_quality_from_list(quals, qn)

        quality_url_map = {int(q): url for q, url in zip(quals, cdn_urls)}
        download_url = quality_url_map[chosen_height]

        if no_title is False:
            safe_title = f"{self.title}.mp4"
            path = os.path.join(path, safe_title)

        try:
            self.core.legacy_download(url=download_url, path=path, callback=callback)
            return True

        except Exception:
            error = traceback.format_exc()
            self.logger.error(error)
            return False





class Client:
    def __init__(self, core: BaseCore = None):
        self.core = core or BaseCore()

    def get_video(self, url: str) -> Video:
        return Video(url, self.core)










