from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def youtubeVideos(api_key, results=10):
   
    youtube = build("youtube", "v3", Key=api_key)

    request = youtube.videos().list(
        part = "snippet",
        chart = "mostPopular",
        maxResults = results
    )
    response = request.execute()

    trendingVideos = {}
    for item in response["items"]:
        thumbnail_url = item["snippet"]["thumbnails"]["high"]["url"]
        title = item["snippet"]["title"]
        trendingVideos[thumbnail_url] = title

    return trendingVideos