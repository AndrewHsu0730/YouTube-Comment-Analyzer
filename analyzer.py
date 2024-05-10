# Package importing
from api_key import API_KEY
from googleapiclient.discovery import build
from googletrans import Translator
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from PIL import Image
import numpy as np
import requests

my_api_key = API_KEY()
youtube = build("youtube", "v3", developerKey=my_api_key)
translator = Translator()
mask = np.array(Image.open("youtube_icon.png"))
stop_words = stopwords.words("english")


# Comment extraction
def extract_data(url, pages):
    original_comments = []
    
    if int(pages) > 2500:
        raise Exception(
            "The number of pages to extract can't exceed 2500 due to quota limit.")

    if "&" in url:
        video_id = url[(url.index("v=") + 2):url.index("&")]
    else:
        video_id = url[(url.index("v=") + 2):]
        
    request = requests.get(f"https://returnyoutubedislikeapi.com/votes?videoId={video_id}").json()
    
    like_count = request["likes"]
    dislike_count = request["dislikes"]
    view_count = request["viewCount"]
    
    n = 0
    while n < int(pages):
        try: 
            cm_request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=response["nextPageToken"]
            )
            
            cm_response = cm_request.execute()
            for item in cm_response["items"]:
                original_comments.append(
                    item["snippet"]["topLevelComment"]["snippet"]["textOriginal"])            
        except:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
            )
            response = request.execute()
            for item in response["items"]:
                original_comments.append(
                    item["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
        n += 1

    return original_comments,like_count,dislike_count,view_count


# Comment translating
def translate_comment(comment):
    if comment != "":
        comment_in_english = translator.translate(comment).text
        return comment_in_english

# Comment processing


def process_comment(df, comment_col):
    url_pattern = r"https?://(www\.)?[-a-zA-Z0-9@:%._\\+~#?&/=]+\.[a-z]{2,6}[-a-zA-Z0-9()@:%._\\+~#?&/=]*"

    df[comment_col] = (
        df[comment_col]
        .str.replace(url_pattern, "", regex=True)
        .str.replace(r"#\S+", "", regex=True)
        .str.replace(r"[^\w\s']+", "", regex=True)
        .str.replace(r"\d+", "", regex=True)
        .str.replace("_", " ")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.lower()
    )

    df[comment_col] = df[df[comment_col] != ""]
    df = df.dropna()
    return df


# Word cloud
def generate_word_cloud(comments):
    word_cloud = WordCloud(scale = 3,
                       collocations = False,
                       background_color = "white",
                       mask = np.array(Image.open('youtube_icon.png')),
                       stopwords = stop_words,
                       colormap = "Reds_r").generate(" ".join(comments))
    plt.figure(figsize=(10,8))
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.title("WordCloud")
    return plt

def calculate_score(df, comment_col):
    analyzer = SentimentIntensityAnalyzer()

    df["Sentiment scores"] = df[comment_col].apply(
        lambda comment: analyzer.polarity_scores(comment))

    df["Compound Scores"] = df["Sentiment scores"].apply(
        lambda sentiment_score: sentiment_score["compound"])

    return df

def identify_sentiment(compound_score):
    if compound_score >= 0.2:
        return "Positive"
    elif compound_score <= -0.2:
        return "Negative"
    else:
        return "Neutral"

def generate_pie_chart(df):
    plt.clf()
    plt.pie(df.values, labels=df.index)
    plt.title("Number of Comments by Sentiment")
    return plt