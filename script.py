# Package importing
from time import time as t
start = t()
import pandas as pd
from api_key import API_KEY
from googleapiclient.discovery import build
from googletrans import Translator
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
end = t()
print("Package importing:", end - start)



# Initialization
start = t()
my_api_key = API_KEY()
youtube = build("youtube", "v3", developerKey = my_api_key)
translator = Translator()
nltk.download("stopwords")
nltk.download("vader_lexicon")
end = t()
print("Initialization:", end - start)



# Comment extraction
start = t()

original_comments = []

def extract_comment(url, pages):
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

comment_list = extract_comment(input("Enter the url of video: "), input("Enter the number of pages to extract: "))

df = pd.DataFrame(comment_list, columns = ["Comments"])

end = t()

print("Comment extraction:", end - start)



# Comment translating
start = t()

def translate_comment(comment):
    comment_in_english = translator.translate(comment).text
    return comment_in_english

df["Comments"] = df["Comments"].apply(translate_comment)

end = t()

print("Comment translating:", end - start)



# Comment processing
start = t()

url_pattern = r"https?://(www\.)?[-a-zA-Z0-9@:%._\\+~#?&/=]+\.[a-z]{2,6}[-a-zA-Z0-9()@:%._\\+~#?&/=]*"

df["Comments"] = (
    df["Comments"]
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

df["Comments"] = df["Comments"].apply(
    lambda comment: " ".join(word for word in comment.split() if word not in stop_words)
)

df["Comments"] = df[df["Comments"] != ""]
df = df.dropna()

end = t()

print("Comment processing:", end - start)



# Word cloud
start = t()

word_cloud = WordCloud(collocations = False, max_words = 30, background_color = "white")

word_cloud.generate(" ".join(df["Comments"]))

plt.imshow(word_cloud, interpolation = "bilinear")
plt.axis("off")
plt.show()

end = t()

print("Word cloud:", end - start)



# Sentiment analysis
start = t()

analyzer = SentimentIntensityAnalyzer()

df["Sentiment scores"] = df["Comments"].apply(lambda comment: analyzer.polarity_scores(comment))

df["Compound Scores"] = df["Sentiment scores"].apply(lambda sentiment_score: sentiment_score["compound"])

def identify_sentiment_of_comment(compound_score):
    if compound_score >= 0.2:
        return "positive"
    elif compound_score <= -0.2:
        return "negative"
    else:
        return "neutral"

df["Sentiments"] = df["Compound Scores"].apply(identify_sentiment_of_comment)

print("Average compound score:", df["Compound Scores"].mean())
print(df.columns)

sentiment_count_df = df["Sentiments"].value_counts().sort_index(ascending = False)

plt.bar(sentiment_count_df.index, sentiment_count_df.values, 0.4)
plt.title("Number of Comments by Sentiment")
plt.show()

end = t()

print("Sentiment analysis:", end - start)