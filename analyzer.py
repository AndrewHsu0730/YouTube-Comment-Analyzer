# Package importing
import pandas as pd
from api_key import API_KEY
from googleapiclient.discovery import build
from googletrans import Translator
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from PIL import Image
import numpy as np



# Initialization
my_api_key = API_KEY()
youtube = build("youtube", "v3", developerKey = my_api_key)
translator = Translator()
#nltk.download("stopwords")
#nltk.download("vader_lexicon")



# Comment extraction
def extract_comment(url, pages):
    original_comments = []

    if int(pages) > 2500:
        raise Exception("The number of pages to extract can't exceed 2500 due to quota limit.") 
    
    if "&" in url:
        video_id = url[(url.index("v=") + 2):url.index("&")]
    else:
        video_id = url[(url.index("v=") + 2):]

    request = youtube.commentThreads().list(
        part = "snippet",
        videoId = video_id,
        maxResults = 100
    )
    response = request.execute()
    for item in response["items"]:
        original_comments.append(item["snippet"]["topLevelComment"]["snippet"]["textOriginal"])

    n = 1
    while n < int(pages):
        request = youtube.commentThreads().list(
            part = "snippet",
            videoId = video_id,
            maxResults = 100,
            pageToken = response["nextPageToken"]
        )
        response = request.execute()
        for item in response["items"]:
            original_comments.append(item["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
        n += 1

    return original_comments

# comment_list = extract_comment(input("Enter the url of video: "), input("Enter the number of pages to extract: "))

# df = pd.DataFrame(comment_list, columns = ["Comments"])



# Comment translating
def translate_comment(comment):
    if comment != "":
        comment_in_english = translator.translate(comment).text
        return comment_in_english

# df["Comments"] = df["Comments"].apply(translate_comment)



# Comment processing
def process_comment(df, comment_col):
    url_pattern = r"https?://(www\.)?[-a-zA-Z0-9@:%._\\+~#?&/=]+\.[a-z]{2,6}[-a-zA-Z0-9()@:%._\\+~#?&/=]*"

    df[comment_col] = (
        df[comment_col]
        .str.replace(url_pattern, "", regex = True)
        .str.replace(r"#\S+", "", regex = True)
        .str.replace(r"[^\w\s']+", "", regex = True)
        .str.replace(r"\d+", "", regex = True)
        .str.replace("_", " ")
        .str.replace(r"\s+", " ", regex = True)
        .str.strip()
        .str.lower()
    )

    stop_words = stopwords.words("english")

    df[comment_col] = df[comment_col].apply(
        lambda comment: " ".join(word for word in comment.split() if word not in stop_words)
    )

    df[comment_col] = df[df[comment_col] != ""]
    df = df.dropna()
    return df



# Word cloud
def generate_word_cloud(comments):
    word_cloud = WordCloud(collocations = False, max_words = 30, background_color = "white")

    word_cloud.generate(" ".join(comments))

    plt.imshow(word_cloud, interpolation = "bilinear")
    plt.axis("off")
    return plt
# plt.show()



# Sentiment analysis
def calculate_score(df, comment_col):
    analyzer = SentimentIntensityAnalyzer()

    df["Sentiment scores"] = df[comment_col].apply(lambda comment: analyzer.polarity_scores(comment))

    df["Compound Scores"] = df["Sentiment scores"].apply(lambda sentiment_score: sentiment_score["compound"])

    return df

def identify_sentiment(compound_score):
    if compound_score >= 0.2:
        return "positive"
    elif compound_score <= -0.2:
        return "negative"
    else:
        return "neutral"

# df["Sentiments"] = df["Compound Scores"].apply(identify_sentiment)

# print("Average compound score:", df["Compound Scores"].mean())
# print(df.columns)

# sentiment_count_df = df["Sentiments"].value_counts().sort_index(ascending = False)

def generate_bar_chart(df):
    plt.clf()
    plt.bar(df.index, df.values, 0.4)
    plt.title("Number of Comments by Sentiment")
    return plt