<h1 align="center">Porntrex API</h1> 

<div align="center">
    <a href="https://pepy.tech/project/porntrex_api"><img src="https://static.pepy.tech/badge/porntrex_api" alt="Downloads"></a>
    <a href="https://github.com/EchterAlsFake/porntrex_api/workflows/"><img src="https://github.com/EchterAlsFake/porntrex_api/workflows/CodeQL/badge.svg" alt="CodeQL Analysis"/></a>
    <a href="https://github.com/EchterAlsFake/porntrex_api/actions/workflows/sync-tests.yml"><img src="https://github.com/EchterAlsFake/porntrex_api/actions/workflows/sync-tests.yml/badge.svg" alt="Sync API Tests"/></a>
</div>

# Description
Porntrex API is an API for porntrex.com. It allows you to fetch information from videos using httpx and Beautifulsoup.

# Disclaimer
> [!IMPORTANT] 
> Porntrex API is in violation to the ToS of porntrex.com!
> If you are the website owner of porntrex.com, contact me at my E-Mail, and I'll take this repository immediately offline.
> EchterAlsFake@proton.me

# Features
- Fetch Video Information
- Download videos
- Fetch Model information
- Download Model videos
- Fetch Channel information
- Download Channel videos
- Search for videos
- Proxy Support
- Http2 support
- Very good code quality with almost perfect type hinting

# Quickstart

### Have a look at the [Documentation](https://github.com/EchterAlsFake/API_Docs/blob/master/Porn_APIs/Porntrex.md) for more details
- Install the library with `pip install porntrex_api`


```python
from porntrex_api import Client
# Initialize a Client object
client = Client()

# Fetch a video
video_object = client.get_video("<insert_url_here>")

# Information from Video objects
print(video_object.title)
print(video_object.duration)
# Download the video

video_object.download(quality="best", path="your_output_path + filename")

# SEE DOCUMENTATION FOR MORE
```

# Support (Donations)
I am developing all my projects entirely for free. I do that because I have fun and I don't want
to charge 30€ like other people do.

However, if you find my work useful, please consider donating something. A tiny amount such as 1€
means a lot to me.

- Paypal: https://paypal.me/EchterAlsFake
- Ko-Fi: https://ko-fi.com/EchterAlsFake
- XMR (Monero): `42XwGZYbSxpMvhn9eeP4DwMwZV91tQgAm3UQr6Zwb2wzBf5HcuZCHrsVxa4aV2jhP4gLHsWWELxSoNjfnkt4rMfDDwXy9jR`


# Contribution
Do you see any issues or having some feature requests? Simply open an Issue or talk
in the discussions.

Pull requests are also welcome.

# License
Licensed under the LGPLv3 License
<br>Copyright (C) 2025 Johannes Habel
