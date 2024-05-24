import re
import requests
import numpy as np
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from googleapiclient.discovery import build
from api_key import API_KEY
import matplotlib.ticker as ticker
import matplotlib
matplotlib.use('Agg')


my_api_key = API_KEY()
youtube = build("youtube", "v3", developerKey=my_api_key)
mask = np.array(Image.open("youtube_icon.png"))
stopwords = stopwords.words("english")
analyzer = SentimentIntensityAnalyzer()


def getStat(vid):
    request = requests.get(
        f"https://returnyoutubedislikeapi.com/votes?videoId={vid}").json()

    like_count = request["likes"]
    dislike_count = request["dislikes"]
    view_count = request["viewCount"]

    return like_count, dislike_count, view_count


def urlToVid(url):
    if url.startswith("https://www.youtube.com/watch?v="):
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


def getTitle(vid):
    response = youtube.videos().list(
        part="snippet",
        id=vid,
    ).execute()
    title = response["items"][0]["snippet"]["title"]
    return title


def getComment(vid, pages):
    word_comments = {}
    comments = []

    if int(pages) > 2500:
        print("Exceed Limit")
        return

    n = 0
    next_page_token = None

    while n < int(pages):
        try:
            if next_page_token:
                response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=vid,
                    maxResults=100,
                    pageToken=next_page_token
                ).execute()
            else:
                response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=vid,
                    maxResults=100
                ).execute()
            
            for item in response["items"]:
                sentence = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                sentence = processComment(sentence)
                if sentence and sentence.strip():
                    comments.append(sentence)
                    for word in sentence.split():
                        if word not in stopwords:
                            word_comments[word.title()] = word_comments.get(word.title(), 0) + 1
            
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break  
            
            n += 1
        
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return word_comments, comments


def generateWordCloud(comments):
    plt.clf()
    plt.subplots(figsize=(12, 6))
    try:
        word_cloud = WordCloud(font_path='arial',
                            scale=3,
                            collocations=False,
                            background_color="white",
                            mask=np.array(Image.open('youtube_icon.png')),
                            colormap="Reds_r").generate_from_frequencies(comments)
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.title("Common Words")
    except:
        word_cloud = WordCloud(scale=3,
                            collocations=False,
                            background_color="white",
                            mask=np.array(Image.open('youtube_icon.png')),
                            colormap="Reds_r").generate_from_frequencies(comments)
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.title("Common Words")
    return plt


def calculateScore(comments):
    scores = list(map(analyzer.polarity_scores, comments))
    sum = 0
    for score in scores:
        sum += score["compound"]
    avg_score = sum / len(scores)
    print(avg_score)
    sentiment = list(
        map(lambda score: identifySentiment(score["compound"]), scores))
    sentimentDict = {"Postive": sentiment.count("Positive"),
                     "Negative": sentiment.count("Negative"),
                     "Neutral": sentiment.count("Neutral")}
    return sentimentDict, avg_score


def identifySentiment(score):
    if score >= 0.2:
        return "Positive"
    elif score <= -0.2:
        return "Negative"
    else:
        return "Neutral"



def getPieChart(sentimentDict):
    total_comments = sum(sentimentDict.values())
    
    sentiment_percentages = {k: (v / total_comments) * 100 for k, v in sentimentDict.items()}
    
    # Plot the pie chart
    plt.clf()
    plt.subplots(figsize=(8, 8))
    plt.pie(sentiment_percentages.values(), labels=sentiment_percentages.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("Percentage of Comments by Sentiment")
    
    return plt


def getBarChart(sentimentDict):
    plt.clf()
    plt.subplots(figsize=(12, 6))
    plt.bar(sentimentDict.keys(), sentimentDict.values(), 0.4)
    plt.title("Number of Comments by Sentiment as a bar chart")
    return plt


def getCommonChart(word_comments):
    plt.clf()
    plt.subplots(figsize=(12, 6))
    res = dict(sorted(word_comments.items(),
               key=lambda x: x[1], reverse=True)[:5])
    plt.bar(list(res.keys()), list(res.values()), 0.5)
    plt.title("Top 5 most used words")
    return plt


def retrieveData(current_uid, url):
    from models import Video
    videos_with_same_url = Video.query.filter_by(
        url=url, user_id=current_uid).all()
    dates_list = [video.date for video in videos_with_same_url]
    likes_list = [video.likes for video in videos_with_same_url]
    dislikes_list = [video.dislikes for video in videos_with_same_url]
    views_list = [video.views for video in videos_with_same_url]
    scores_list = [video.score for video in videos_with_same_url]
    return getStats(dates_list, likes_list, dislikes_list, views_list)


def getStats(date, likes, dislike, view):
    plt.clf()
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.bar(date, dislike, width=0.4, label='Dislikes',color = "red")
    ax1.bar(date, likes, bottom=dislike, width=0.4, label='Likes',color = "green")
    ax2 = ax1.twinx()
    ax2.plot(date, view, color='y', label='Views',color = "blue")
    fig.tight_layout()
    formatter = ticker.FuncFormatter(lambda x, pos: '{:,.1f}'.format(
        x / 1000) + 'K' if x < 1000000 else '{:,.1f}M'.format(x / 1000000) if x < 1000000000 else '{:,.1f}B'.format(x / 1000000000))
    ax1.yaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter(formatter)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    return plt


def getAllChart(word_comments, sentimentDict, uid, url):
    import os
    
    wc = generateWordCloud(word_comments)  # Generate word cloud
    wc.savefig(os.path.join("static", "images", "word_cloud.png")) # Save the word cloud
    
    pie_chart = getPieChart(sentimentDict)  # Generate pie chart
    pie_chart.savefig(os.path.join("static", "images",
                      "pie_chart.png"))  # Save the pie chart
    
    #bar_chart = getBarChart(sentimentDict)  # Generate bar chart
    #bar_chart.savefig(os.path.join("static", "images","bar_chart.png"))  # Save the bar chart

    common_chart = getCommonChart(word_comments)  # Generate common chart
    common_chart.savefig(os.path.join("static", "images", "common_chart.png")) # Save the common chart
    
    stats = retrieveData(uid, url)
    stats.savefig(os.path.join("static", "images", "stats.png"))
