import matplotlib
matplotlib.use('Agg')
from api_key import API_KEY
from googleapiclient.discovery import build
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from PIL import Image
import numpy as np
import requests
import re


my_api_key = API_KEY()
youtube = build("youtube", "v3", developerKey=my_api_key)
mask = np.array(Image.open("youtube_icon.png"))
stopwords = stopwords.words("english")
analyzer = SentimentIntensityAnalyzer()

def getStat(vid):
    request = requests.get(f"https://returnyoutubedislikeapi.com/votes?videoId={vid}").json()
    
    like_count = request["likes"]
    dislike_count = request["dislikes"]
    view_count = request["viewCount"]
    
    return like_count,dislike_count,view_count

def urlToVid(url):
    if "&" in url:
        vid = url[(url.index("v=") + 2):url.index("&")]
    else:
        vid = url[(url.index("v=") + 2):]
    return vid


def processComment(comment):
    url_pattern = r"https?://(www\.)?[-a-zA-Z0-9@:%._\\+~#?&/=]+\.[a-z]{2,6}[-a-zA-Z0-9()@:%._\\+~#?&/=]*"
    comment = re.sub(url_pattern, "", comment)
    comment = re.sub(r"#\S+", "", comment)
    comment = re.sub(r"[^\w\s']+", "", comment)
    comment = re.sub(r"\d+", "", comment)
    comment = comment.replace("_", " ")
    comment = re.sub(r"\s+", " ", comment)
    comment = comment.strip().lower()
    
    return comment


    

def getComment(vid, pages):
    word_comments = {}
    comments = []
    if int(pages) > 2500:
        raise Exception(
            "The number of pages to extract can't exceed 2500 due to limit.")
    n = 0
    
    while n < int(pages):
        try: 
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=vid,
                maxResults=100,
                pageToken=response["nextPageToken"]
            ).execute()
        
            for item in response["items"]:
                sentence = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                sentence = processComment(sentence)
                if sentence == "" or sentence == " ":
                    pass
                else:
                    comments.append(sentence)
                    for word in sentence.split():
                        if word not in stopwords:
                            word_comments[word] = word_comments.get(word,0) + 1
        except:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=vid,
                maxResults=100,
            ).execute()
            for item in response["items"]:
                sentence = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                sentence = processComment(sentence)
                if sentence == "" or sentence == " ":
                    pass
                else:
                    comments.append(sentence)
                    for word in sentence.split():
                        if word not in stopwords:
                            word_comments[word] = word_comments.get(word,0) + 1
        n += 1
    return word_comments,comments

def generateWordCloud(comments):
    plt.clf()
    word_cloud = WordCloud(scale = 3,
                       collocations = False,
                       background_color = "white",
                       mask = np.array(Image.open('youtube_icon.png')),
                       colormap = "Reds_r").generate_from_frequencies(comments)
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.title("Common Words")
    return plt

def calculateScore(comments):
    scores = list(map(analyzer.polarity_scores,comments))
    print(scores)
    sentiment = list(map(lambda score:identifySentiment(score["compound"]),scores))
    sentimentDict = {"Postive":sentiment.count("Positive"),
                     "Negative":sentiment.count("Negative"),
                     "Neutral":sentiment.count("Neutral")}
    print(sentimentDict)
    return sentimentDict

def identifySentiment(score):
    if score >= 0.2:
        return "Positive"
    elif score <= -0.2:
        return "Negative"
    else:
        return "Neutral"

def getPieChart(sentimentDict):
    plt.clf()
    plt.pie(sentimentDict.values(), labels=sentimentDict.keys())
    plt.title("Number of Comments by Sentiment")
    return plt

def getStats (date,likes,dislike,view):
    fig,ax1 = plt.subplots()
    ax1.bar(date,dislike,width = 0.4)
    ax1.bar(date,likes,bottom = dislike, width = 0.4)
    ax2 = ax1.twinx()
    ax2.plot(date,view,color='y')
    fig.tight_layout()
    plt.show()