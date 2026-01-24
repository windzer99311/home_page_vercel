import requests
import re
import json
from fastapi import FastAPI
app = FastAPI()
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
    # print(data)
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
        Url=item[case]["navigationEndpoint"]["watchEndpoint"]["videoId"]
        home_data.append({"title":title,"thumbnail":Thumbnail,"videoId":Url})
    return   {
    "data": home_data,
    }
@app.get("/next")
def get_next_music(url: str):
    next_music = []
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers).text

    # Extract ytInitialData
    pattern = r'var ytInitialData = ({.*?});'
    match = re.search(pattern, response)
    if match:
        json_str = match.group(1)
        data = json.loads(json_str)
        playlist = data["contents"]["twoColumnWatchNextResults"]["secondaryResults"]["secondaryResults"]["results"]
        for item in playlist:
            try:
                title=item["lockupViewModel"]["metadata"]["lockupMetadataViewModel"]["title"]["content"]
                Thumbnail="Thumbnail:",item["lockupViewModel"]["contentImage"]["thumbnailViewModel"]["image"]["sources"][0]["url"]
                Url=item["lockupViewModel"]["metadata"]["lockupMetadataViewModel"]["menuButton"]["buttonViewModel"]["onTap"]["innertubeCommand"]["showSheetCommand"]["panelLoadingStrategy"]["inlineContent"]["sheetViewModel"]["content"]["listViewModel"]["listItems"][0]["listItemViewModel"]["rendererContext"]["commandContext"]["onTap"]["innertubeCommand"]["signalServiceEndpoint"]["actions"][0]["addToPlaylistCommand"]["videoId"]
                next_music.append({"title": title, "thumbnail": Thumbnail, "videoId": Url})
            except:
                continue
        return {
            "data": next_music,
        }
