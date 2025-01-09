import os
import re
import requests
import numpy as np
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from nltk.corpus import stopwords
from googleapiclient.discovery import build
from api_key import API_KEY
from models import Video
from database import db
from sqlalchemy import select, func
import matplotlib.pyplot as plt
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
        f"https://returnyoutubedislikeapi.com/votes?videoId={vid}"
    ).json()

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
    else:
        return None


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
    if response["items"] == []:
        return None
    title = response["items"][0]["snippet"]["title"]
    return title


def getThumbnail(vid):
    thumnail_url = "http://img.youtube.com/vi/%s/0.jpg" % vid
    return thumnail_url


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

    plt.subplots(figsize=(5, 5))
    try:
        word_cloud = WordCloud(
            font_path='arial',
            scale=3,
            collocations=False,
            background_color="white",
            mask=np.array(Image.open('youtube_icon.png')),
            colormap="Reds_r"
        ).generate_from_frequencies(comments)
    except:
        word_cloud = WordCloud(
            scale=3,
            collocations=False,
            background_color="white",
            mask=np.array(Image.open('youtube_icon.png')),
            colormap="Reds_r"
        ).generate_from_frequencies(comments)

    plt.imshow(word_cloud)
    plt.axis('off')
    return plt


def calculateScore(comments):
    scores = list(map(analyzer.polarity_scores, comments))
    sum_ = 0
    for score in scores:
        sum_ += score["compound"]
    avg_score = sum_ / len(scores)
    sentiment = list(map(lambda score: identifySentiment(score["compound"]), scores))
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
    plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = plt.pie(sentiment_percentages.values(),
                                       labels=sentiment_percentages.keys(),
                                       autopct='%1.1f%%',
                                       startangle=140,
                                       textprops=dict(color="white", weight='bold'))

    # Change the color and weight of the labels
    for text in texts:
        text.set_color('white')
        text.set_weight('bold')

    for i, autotext in enumerate(autotexts):
        percentage_value = list(sentiment_percentages.values())[i]
        autotext.set_text(f'{percentage_value:.1f}% ')
        autotext.set_color('white')
        autotext.set_weight('bold')
        autotext.set_size(10)
    plt.legend(loc='upper right')
    return plt


def getStats(dates, likes, dislikes, views):
    plt.clf()

    # Dynamic figure width based on number of data points
    num_data_points = len(dates)
    fig_width = max(10, num_data_points / 5)

    # Height is fixed, width is dynamic
    fig, ax1 = plt.subplots(figsize=(fig_width, 6))

    # Get x positions for bars
    bar_positions = range(len(dates))

    # Plot dislikes bar in red
    bars_dislikes = ax1.bar(bar_positions, dislikes, width=0.4, label='Dislikes', color='red')

    # Plot likes bar in green, stacked on top of dislikes
    bars_likes = ax1.bar(bar_positions, likes, bottom=dislikes, width=0.4, label='Likes', color='green')

    # Plot views on a secondary y-axis
    ax2 = ax1.twinx()
    line_views, = ax2.plot(bar_positions, views, label='Views', color='blue', marker='o')

    # Annotate the bars with the actual numbers only when values change
    last_likes_value = None
    last_dislikes_value = None

    for bar_likes, bar_dislikes, xpos in zip(bars_likes, bars_dislikes, bar_positions):
        # Likes
        if last_likes_value is None or bar_likes.get_height() != last_likes_value:
            height_likes = bar_likes.get_height() + bar_likes.get_y()
            ax1.annotate(f'{int(bar_likes.get_height())}',
                         xy=(xpos + bar_likes.get_width() / 2,
                             height_likes - bar_likes.get_height() / 2),
                         xytext=(0, 3), textcoords="offset points", ha='center', va='top', color='black', weight='bold')
            last_likes_value = bar_likes.get_height()

        # Dislikes
        if last_dislikes_value is None or bar_dislikes.get_height() != last_dislikes_value:
            height_dislikes = bar_dislikes.get_height()
            ax1.annotate(f'{int(bar_dislikes.get_height())}',
                         xy=(xpos + bar_dislikes.get_width() / 2,
                             height_dislikes / 2),
                         xytext=(0, 3), textcoords="offset points", ha='center', va='center', color='black', weight='bold')
            last_dislikes_value = bar_dislikes.get_height()

    # Annotate the views on the line plot only when the view value changes
    last_view_value = None
    for xpos, y in zip(bar_positions, views):
        if last_view_value is None or y != last_view_value:
            ax2.annotate(f'{y:,}', xy=(xpos, y), xytext=(0, 10), textcoords='offset points', ha='center', va='bottom', color='blue', weight='bold')
            last_view_value = y

    # Define custom formatter for y-axis to format numbers
    number_formatter = ticker.FuncFormatter(
        lambda x, pos: '{:,.1f}K'.format(x / 1000) if x < 1000000 else '{:,.1f}M'.format(x / 1000000) if x < 1000000000 else '{:,.1f}B'.format(x / 1000000000)
    )
    ax1.yaxis.set_major_formatter(number_formatter)

    # Define custom formatter for secondary y-axis to format views
    views_formatter = ticker.FuncFormatter(
        lambda x, pos: '{:,.1f}K'.format(x / 1000) if x < 1000000 else '{:,.1f}M'.format(x / 1000000) if x < 1000000000 else '{:,.1f}B'.format(x / 1000000000)
    )
    ax2.yaxis.set_major_formatter(views_formatter)

    # Improve layout
    fig.tight_layout()

    # Add legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Rotate date labels for better readability and align with bars
    ax1.set_xticks(bar_positions)
    ax1.set_xticklabels(dates, rotation=45, ha='right')

    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(os.path.join("static", "images", "stats.png"))

    return plt


def getCommonChart(word_comments):
    plt.clf()
    plt.subplots(figsize=(5, 5))
    res = dict(sorted(word_comments.items(),
               key=lambda x: x[1], reverse=True)[:5])
    plt.bar(list(res.keys()), list(res.values()), 0.5)
    return plt


def retrieveData(current_uid, url):
    videos_with_same_url = Video.query.filter_by(url=url, user_id=current_uid).all()
    dates_list = [video.date for video in videos_with_same_url]
    likes_list = [video.likes for video in videos_with_same_url]
    dislikes_list = [video.dislikes for video in videos_with_same_url]
    views_list = [video.views for video in videos_with_same_url]
    return getStats(dates_list, likes_list, dislikes_list, views_list)


def getLatestVideos(current_uid):
    subquery = (
        db.select(Video.url, func.max(Video.date).label("latest_date"))
        .where(Video.user_id == current_uid)
        .group_by(Video.url)
        .subquery()
    )
    latest_videos = (
        db.session.execute(
            db.select(Video)
            .join(subquery, (Video.url == subquery.c.url) & (Video.date == subquery.c.latest_date))
            .where(Video.user_id == current_uid)
        ).scalars()
    )

    return latest_videos


def getAllChart(word_comments, sentimentDict):
    wc = generateWordCloud(word_comments)  
    # Save the word cloud
    wc.savefig(os.path.join("static", "images", "word_cloud.png"))

    pie_chart = getPieChart(sentimentDict)  
    pie_chart.savefig(os.path.join("static", "images", "pie_chart.png")) 

    common_chart = getCommonChart(word_comments) 
    common_chart.savefig(os.path.join("static", "images", "common_chart.png"))
