import requests
import re
import json
from fastapi import FastAPI
app = FastAPI()
from urllib.parse import urlparse, parse_qs

def clean_youtube_url(url: str) -> str | None:
    if url.startswith("/"):
        url = "https://www.youtube.com" + url
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    vid = params.get("v", [None])[0]
    return f"https://www.youtube.com/watch?v={vid}" if vid else None
    
@app.get("/homepage")
def get_playlist(url:str):
    home_data=[]
    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers).text

    # Extract ytInitialData
    m = re.search(r"ytInitialData\s*=\s*(\{.*?\});", html)
    if not m:
        raise Exception("ytInitialData not found")

    data = json.loads(m.group(1))
    print(data)
    if "playnext" in url:
        case1=True
    else:
        case1=False

    if case1:
        case = "playlistPanelVideoRenderer"
        items = data["contents"]["twoColumnWatchNextResults"]["playlist"]["playlist"]["contents"]
    else:
        case= "playlistVideoRenderer"
        items = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"][
            "contents"][0]["itemSectionRenderer"]["contents"][0]["playlistVideoListRenderer"]["contents"]
    for item in items:
        if case1:
            title=item[case]["title"]["simpleText"]
        else:
            title=item[case]["title"]["runs"][0]["text"]
        Thumbnail=item[case]["thumbnail"]["thumbnails"][1]["url"]
        Url=Url=clean_youtube_url(item[case]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"])
        home_data.append({"title":title,"thumbnail":Thumbnail,"url":Url})
    return   {
    "data": home_data,
    }
